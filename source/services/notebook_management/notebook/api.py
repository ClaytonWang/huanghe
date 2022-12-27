# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/15 10:21
"""
import json
from typing import List, Dict
from fastapi import APIRouter, Depends, Request, HTTPException, status, Path
from fastapi.responses import JSONResponse
from models import Notebook, Status, Image, Source
from notebook.serializers import NotebookList, NotebookCreate, NotebookEdit, NotebookOp, NotebookCreateAfter, ImageItem
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from utils.user_request import get_user_list, get_project_list
from utils.storage_request import volume_check
from utils.k8s_request import create_notebook_k8s
from utils.auth import operate_auth
from collections import defaultdict


router_notebook = APIRouter()


@router_notebook.get(
    '',
    description='notebook列表',
    response_model=Page[NotebookList],
    response_model_exclude_unset=True
)
async def list_notebook(request: Request,
                        query_params: QueryParameters = Depends(QueryParameters),
                        ):
    """
    :param request:
    :param query_params:
    :return:
    """
    params_filter = query_params.filter_
    # print(params_filter)
    authorization: str = request.headers.get('authorization')
    role_name = request.user.role.name
    # print(f"role_name: {role_name}")

    user_list = await get_user_list(authorization)
    # print("user_list")
    # print(user_list)
    # 建立映射表
    res_user_map = {x['id']: {'id': x['id'], 'username': x['username']} for x in user_list}
    id_proj_map = {x['id']: x['project_ids'] for x in user_list}
    name_userid_map = defaultdict(list)
    role_userid_map = defaultdict(list)
    for x in user_list:
        name_userid_map[x['username']].append(x['id'])
        role_userid_map[x['role_name']].append(x['id'])
    # print(role_userid_map)

    project_list = await get_project_list(authorization)
    # print("project_list")
    # print(project_list)
    code_id_map = {x['code']: x['id'] for x in project_list}
    res_proj_map = {x['id']: {'id': x['id'], 'name': x['name']} for x in project_list}

    # todo 临时方案,存储image表
    images = await Image.objects.all()
    image_map = {x.id: x.get_dict() for x in images}

    sources = await Source.objects.all()
    source_map = {x.id: x.get_str() for x in sources}

    # 用户可见项目
    if role_name != 'admin':
        viewable_project_ids = id_proj_map.get(request.user.id)
        params_filter['project_id__in'] = viewable_project_ids

    if params_filter:
        name_filter, role_filter = None, None
        if 'name' in params_filter:
            name = params_filter.pop('name')
            name_filter = set(name_userid_map.get(name, []))
        if 'project__code' in params_filter:
            project_code = params_filter.pop('project__code')
            params_filter['project_id'] = code_id_map.get(project_code)
        if 'role__name' in params_filter:
            role__name = params_filter.pop('role__name')
            role_filter = set(role_userid_map.get(role__name, []))
        if not (name_filter is None and role_filter is None):
            creator_ids = list(name_filter.intersection(role_filter)) if not (
                    name_filter is None or role_filter is None) else list(name_filter or role_filter)
            params_filter['creator_id__in'] = creator_ids
    # todo 要修改合理的params_filter，不然会报错
    # print("show filter")
    # print(params_filter)

    result = await paginate(Notebook.objects.select_related(
        'status'
    ).filter(**params_filter), params=query_params.params)
    result = result.dict()
    data = result['data']

    for item in data:
        source_id = item.pop('source')['id']
        item['source'] = source_map.get(source_id)

        creator_id = item.pop('creator_id')
        creator_info = res_user_map.get(creator_id)
        item['creator'] = creator_info

        project_id = item.pop('project_id')
        project_info = res_proj_map.get(project_id)
        item['project'] = project_info

        image_id = item.pop('image_id')
        image_info = image_map.get(image_id)
        item['image'] = image_info
    return result


@router_notebook.post(
    '',
    description='创建Notebook',
    response_model=NotebookCreateAfter,
)
async def create_notebook(request: Request,
                          notebook: NotebookCreate):
    authorization: str = request.headers.get('authorization')
    init_data = notebook.dict()
    init_data['creator_id'] = request.user.id

    stat = await Status.objects.get(name='stopped')
    init_data['status'] = stat.id

    duplicate_name = await Notebook.objects.filter(name=init_data['name']).count()
    if duplicate_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notebook不能重名')

    project_id = int(init_data.pop('project')['id'])
    if request.user.role.name != 'admin' and project_id not in request.user.project_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='不是用户所属项目')
    init_data['project_id'] = project_id

    source = init_data.pop('source')
    sources = await Source.objects.all()
    source_map = {x.get_str(): x for x in sources}
    _source = source_map.get(source)
    init_data['source'] = _source.id

    image_id = init_data.pop('image')['id']
    _image = await Image.objects.get_or_none(pk=int(image_id))
    if not _image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='镜像不存在')
    init_data['image_id'] = image_id

    # 存储检查
    hooks = init_data.pop('hooks')
    storages, volumes_k8s = await volume_check(authorization, hooks)
    init_data['storage'] = json.dumps(storages)

    _notebook = await Notebook.objects.create(**init_data)
    # todo 同notebook集群发送
    payloads = {
        'name': f"{request.user.en_name}-{init_data['name']}",  # todo user的en_name + notebook的name
        'namespace': request.user.project_ids.get(project_id),
        'image': _image.name,
        'env': 'dev',  # todo 填当前环境，从不同环境去读
        'cpu': _source.cpu,
        'memory': _source.memory,
        'gpu': _source.gpu,
        'volumes': volumes_k8s,
    }
    # print(payloads)
    # todo response返回不为200时更新notebook状态到异常
    # response = await create_notebook_k8s(authorization, payloads)
    # if response.status != 200:
    #     _notebook.status = None
    return _notebook


@router_notebook.put(
    '/{notebook_id}',
    description='编辑Notebook',
)
async def update_notebook(request: Request,
                          notebook: NotebookEdit,
                          notebook_id: int = Path(..., ge=1, description="NotebookID"),
                          ):
    # user: AccountGetter = request.user
    authorization: str = request.headers.get('authorization')
    update_data = notebook.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新数据不能为空')

    _notebook, reason = await operate_auth(request, notebook_id)
    if not _notebook:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

    if _notebook.status.name != 'stopped':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notebook未停止')

    if 'name' in update_data:
        duplicate_name = await Notebook.objects.filter(name=update_data['name']).count()
        if duplicate_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notebook不能重名')

    if 'projects' in update_data:
        project_id = update_data.pop('project')['id']
        if request.user.role.name != 'admin' and int(project_id) not in request.user.project_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='不是用户所属项目')
        update_data['project_id'] = project_id

    if 'source' in update_data:
        source = update_data.pop('source')
        sources = await Source.objects.all()
        source_map = {x.get_str(): x.id for x in sources}
        update_data['source'] = source_map.get(source)

    if 'image' in update_data:
        image_id = update_data.pop('image')['id']
        _image = await Image.objects.get_or_none(pk=int(image_id))
        if not _image:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='镜像不存在')
        update_data['image_id'] = image_id

    if 'hooks' in update_data:
        hooks = update_data.pop('hooks')
        storages, volumes_k8s = await volume_check(authorization, hooks)
        update_data['storage'] = json.dumps(storages)

    if not await _notebook.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notebook不存在')
    # todo 更新notebook集群
    return JSONResponse(dict(id=notebook_id))


@router_notebook.post(
    '/{notebook_id}',
    description='启动/停止Notebook',
)
async def operate_notebook(request: Request,
                           data: NotebookOp,
                           notebook_id: int = Path(..., ge=1, description="NotebookID")):
    action = int(data.dict()['action'])
    update_data = {}
    _notebook, reason = await operate_auth(request, notebook_id)
    if not _notebook:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    if action not in [0, 1]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')

    if _notebook.status.name == 'running' and int(action) == 0:
        stat = await Status.objects.get(name='stop')
        update_data['status_id'] = stat.id
    elif _notebook.status.name == 'stopped' and int(action) == 1:
        # TODO 做一大堆启动操作，包含volume启动与状态轮训
        stat = await Status.objects.get(name='start')
        update_data['status_id'] = stat.id

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新数据不能为空')
    if not await _notebook.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notebook不存在')
    return JSONResponse(dict(id=notebook_id))


@router_notebook.delete(
    '/{notebook_id}',
    description='删除Notebook',
)
async def delete_notebook(request: Request,
                          notebook_id: int = Path(..., ge=1, description="NotebookID")):
    _notebook, reason = await operate_auth(request, notebook_id)
    if not _notebook:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    await _notebook.delete()


@router_notebook.get(
    '/source',
    description='资源规格列表',
)
async def list_source():
    query = await Source.objects.all()
    data = [x.get_str() for x in query]
    return {"data": data}


@router_notebook.get(
    '/images',
    description='镜像列表',
    response_model=Page[ImageItem],
    response_model_exclude_unset=True
)
async def list_images(query_params: QueryParameters = Depends(QueryParameters),):
    params_filter = query_params.filter_
    result = await paginate(Image.objects.filter(**params_filter), params=query_params.params)
    return result
