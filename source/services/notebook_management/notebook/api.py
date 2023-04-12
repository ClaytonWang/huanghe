# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/15 10:21
"""
import ujson as json
from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException, status, Path, Query
from fastapi.responses import JSONResponse
from models import Notebook, Status, Image
from notebook.serializers import NotebookList, NotebookCreate, NotebookEdit, NotebookOp, NotebookDetail, EventItem, \
    EventCreate, NotebookSimple
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from basic.common.event_model import Event
from basic.common.env_variable import get_string_variable
from basic.middleware.account_getter import AccountGetter, ProjectGetter, get_project
from basic.middleware.service_requests import get_user_list, volume_check
from utils.user_request import project_check, project_check_obj
from utils.k8s_request import create_notebook_k8s, delete_notebook_k8s
from utils.auth import operate_auth
from collections import defaultdict
import datetime

router_notebook = APIRouter()
COMMON = "https://grafana.digitalbrain.cn:32443/d-solo/3JLLppA4k/notebookjian-kong?"
ACCOUNT = "jovyan"
PASSWORD = "jovyan"


@router_notebook.get(
    '/project_backend/{project_id}',
    description='通过项目查询nb',
)
async def list_nb_by_project(project_id: int = Path(..., ge=1, description='需要查询项目的project id'),
                             user_id: int = Query(None, description='用户id')) -> bool:
    if user_id:
        nc = await Notebook.self_project_and_self_view(project_id=project_id, self_id=user_id)
    else:
        nc = await Notebook.self_project(project_id)
    if not nc:
        return False
    return True


@router_notebook.get(
    '/by_server/{server_ip}',
    description='通过节点IP查询nb',
)
async def list_nb_by_server(server_ip: str = Path(..., description='需要查询项目的server_ip')):
    return await Notebook.project_list_by_ip(server_ip)


def format_notebook_detail(nb: Notebook):
    result = nb.dict()
    result.update({
        'source': nb.get_source(),
        'project': {
            'id': nb.project_by_id,
            'name': nb.project_by,
        },
        'image': {
            'desc': '',
            'name': nb.image,
            'custom': nb.custom,
        },
        'creator': {
            'id': nb.created_by_id,
            'username': nb.created_by,
        },
        'hooks': result['storage'],
        'grafana': {
            'cpu': nb.cpu_url(COMMON),
            'ram': nb.ram_url(COMMON),
            'gpu': nb.gpu_url(COMMON),
            'vram': nb.vram_url(COMMON),
        },
        'ssh': {
            'account': ACCOUNT,
            'password': PASSWORD,
            'address': nb.pod_ip,
        },
    })
    return result


@router_notebook.get(
    '/volume/{volume_id}',
    description='存储-notebook列表',
)
async def get_volume_notebook(volume_id: int = Path(..., ge=1, description='需要查询的存储 ID')):
    _notebook = await Notebook.objects.all()
    storage_list = [(x.storage, x.id) for x in _notebook]
    volume_note_dict = defaultdict(set)
    for storage, notebook_id in storage_list:
        for x in storage:
            volume_note_dict[x['storage']['id']].add(notebook_id)
    note_ids = volume_note_dict.get(volume_id, [])
    if not note_ids:
        return []
    note_map = {x.id: {'id': x.id, 'name': x.name} for x in _notebook}
    result = [note_map[x] for x in note_ids]
    return result


@router_notebook.get(
    '/items',
    description='notebook概况',
    response_model=List[NotebookSimple],
    response_model_exclude_unset=True
)
async def get_simple_notebook(query_params: QueryParameters = Depends(QueryParameters),):
    params_filter = query_params.filter_

    if params_filter:
        if 'creator_id' in params_filter:
            creator_id = params_filter.pop('creator_id')
            params_filter['created_by_id'] = int(creator_id)
        if 'project_ids' in params_filter:
            project_ids = params_filter.pop('project_ids')
            if isinstance(project_ids, str):
                project_ids = [int(x) for x in project_ids.split(',')]
            params_filter['project_by_id__in'] = project_ids

    query = await Notebook.objects.select_related('status').filter(**params_filter).all()

    return [x.get_dict() for x in query]


@router_notebook.get(
    '/{notebook_id}',
    description="notebook详情",
    response_model=NotebookDetail,
    response_model_exclude_unset=True
)
async def get_notebook(notebook_id: int = Path(..., ge=1, description='需要查询的notebook ID')):
    _notebook = await Notebook.objects.select_related(['status']).get(pk=notebook_id)
    return format_notebook_detail(_notebook)


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
    authorization: str = request.headers.get('authorization')
    role_name = request.user.role.name

    user_list = await get_user_list(authorization)
    id_proj_map = {x['id']: x['project_ids'] for x in user_list}

    # 用户可见项目
    if role_name != 'admin':
        viewable_project_ids = id_proj_map.get(request.user.id)
        params_filter['project_by_id__in'] = viewable_project_ids
        params_filter['created_by_id'] = request.user.id

    result = await paginate(Notebook.objects.select_related(
        'status'
    ).order_by(Notebook.updated_at.desc()).filter(**params_filter), params=query_params.params)
    result = result.dict()
    data = result['data']

    for item in data:
        cpu = item["cpu"]
        memory = item["memory"]
        if item['type'] != "CPU":
            gpu = item['gpu']
            machine_type = item['type']
            item['source'] = f"GPU {gpu}*{machine_type} {cpu}C {memory}G"
        else:
            item['source'] = f"CPU {cpu}C {memory}G"
        item['creator'] = {
            "id": int(item["created_by_id"]),
            "username": item["created_by"],
        }
        item['image'] = {
            'name': item['image'],
            'desc': "",
            # "custom": item['custom'],
        }
        item['project'] = {
            'id': int(item['project_by_id']),
            'name': item['project_by'],
        }

    return result


@router_notebook.post(
    '',
    description='创建Notebook',
    response_model=NotebookDetail,
)
async def create_notebook(request: Request,
                          nc: NotebookCreate):
    authorization: str = request.headers.get('authorization')
    init_data = {"name": nc.name}
    ag: AccountGetter = request.user
    init_data['created_by_id'] = ag.id
    init_data['updated_by_id'] = ag.id
    init_data['create_en_by'] = ag.en_name
    init_data['created_by'] = ag.username
    init_data['updated_by'] = ag.username
    stat = await Status.objects.get(name='stopped')
    init_data['status'] = stat.id

    check, extra_info = await project_check(request, nc.project.id)
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info)
    pg: ProjectGetter = get_project(request.headers.get('authorization'), nc.project.id)
    init_data['project_by_id'] = pg.id
    init_data['project_by'] = pg.name
    init_data['project_en_by'] = pg.en_name

    if await Notebook.objects.filter(name=init_data['name'], project_by_id=int(nc.project.id),
                                     created_by_id=ag.id).count():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='同一个项目下，同一个用户，Notebook不能重名')

    gpu_count = 0
    if nc.source.startswith("GPU"):
        machine_type = "GPU"
        _, gpu_count, cpu_count, memory = nc.source.split()
        gpu_count = gpu_count.split("*")[0]
        cpu_count = cpu_count.split("C")[0]
        memory = memory.split("G")[0]
    else:
        machine_type = "CPU"
        _, cpu_count, memory = nc.source.split()
        cpu_count = cpu_count.split("C")[0]
        memory = memory.split("G")[0]
    init_data["cpu"] = cpu_count
    init_data["gpu"] = gpu_count
    init_data["memory"] = memory
    init_data["type"] = machine_type

    # image_id = int(init_data.pop('image'))
    # image = await Image.objects.get_or_none(pk=image_id)
    # if not image:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='镜像不存在')
    init_data['image'] = nc.image.name
    init_data['custom'] = nc.image.custom

    # 存储检查
    storages, volumes_k8s = await volume_check(authorization, nc.hooks, extra_info)
    init_data['storage'] = json.dumps(storages)

    k8s_info = {
        'name': f"{request.user.en_name}-{init_data['name']}",
        'namespace': extra_info,
        'image': nc.image.name,
        'env': get_string_variable('ENV', 'DEV').lower(),
        'cpu': cpu_count,
        'memory': memory,
        'gpu': gpu_count,
        'type': machine_type,
        'volumes': volumes_k8s,
        'annotations': {"notebooks.kubeflow.org/http-rewrite-uri": "/"} if "codeserver" in nc.image.name else {},
    }
    init_data['k8s_info'] = json.dumps(k8s_info)

    _notebook = await Notebook.objects.create(**init_data)
    k8s_info['annotations'].update({"id": str(_notebook.id)})
    await _notebook.update(**{"k8s_info": k8s_info})
    return format_notebook_detail(_notebook)


@router_notebook.put(
    '/{notebook_id}',
    description='编辑Notebook',
)
async def update_notebook(request: Request,
                          ne: NotebookEdit,
                          notebook_id: int = Path(..., ge=1, description="NotebookID"),
                          ):
    # user: AccountGetter = request.user
    authorization: str = request.headers.get('authorization')
    ag: AccountGetter = request.user
    update_data = ne.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新数据不能为空')

    _notebook, reason = await operate_auth(request, notebook_id)
    if not _notebook:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    k8s_info = _notebook.k8s_info

    if _notebook.status.name != 'stopped':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notebook未停止')

    project_id = ne.project.id
    check, extra_info = await project_check_obj(request, project_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info)
    update_data.update({"project_by_id": project_id,
                        "project_by": extra_info['name'],
                        "project_en_by": extra_info['en_name']})
    if 'project' in update_data:
        update_data.pop('project')
    k8s_info['namespace'] = extra_info['en_name']

    duplicate_name = await Notebook.objects.filter(
        name=update_data['name'], project_by_id=int(project_id), created_by_id=ag.id).exclude(id=_notebook.id).count()
    if duplicate_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='同一个项目下，同一个用户，Notebook不能重名')
    k8s_info['name'] = f"{ag.en_name}-{update_data['name']}"

    if ne.source:
        gpu_count = 0
        if ne.source.startswith("GPU"):
            machine_type = "GPU"
            _, gpu_count, cpu_count, memory = ne.source.split()
            gpu_count = gpu_count.split("*")[0]
            cpu_count = cpu_count.split("C")[0]
            memory = memory.split("G")[0]
        else:
            machine_type = "CPU"
            _, cpu_count, memory = ne.source.split()
            cpu_count = cpu_count.split("C")[0]
            memory = memory.split("G")[0]
        update_data["cpu"] = cpu_count
        update_data["gpu"] = gpu_count
        update_data["memory"] = memory
        update_data["type"] = machine_type
        k8s_info.update({
            'cpu': cpu_count,
            'memory': memory,
            'gpu': gpu_count,
            'type': machine_type,
        })
    if 'source' in update_data:
        update_data.pop('source')
    update_data['image'] = ne.image.name
    update_data['custom'] = ne.image.custom
    k8s_info['image'] = ne.image.name

    update_data.pop('hooks')
    storages, volumes_k8s = await volume_check(authorization, ne.hooks, extra_info['en_name'])

    update_data['storage'] = json.dumps(storages)
    k8s_info['volumes'] = volumes_k8s
    k8s_info['annotations'] = {"notebooks.kubeflow.org/http-rewrite-uri": "/"} if "codeserver" in ne.image.name else {}

    update_data['k8s_info'] = json.dumps(k8s_info)
    update_data['updated_at'] = datetime.datetime.now()

    if not await _notebook.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notebook不存在')
    return JSONResponse(dict(id=notebook_id))


@router_notebook.post(
    '/{notebook_id}',
    description='启动/停止Notebook',
)
async def operate_notebook(request: Request,
                           data: NotebookOp,
                           notebook_id: int = Path(..., ge=1, description="NotebookID")):
    authorization: str = request.headers.get('authorization')
    action = int(data.dict()['action'])
    _notebook, reason = await operate_auth(request, notebook_id)
    if not _notebook:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    if action not in [0, 1]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')
    payloads = json.dumps(_notebook.k8s_info)

    # 数字，0（停止）｜1（启动）
    update_data = {}
    if action == 0:
        if _notebook.status.name not in ['start', 'running', 'pending']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')
        stat = await Status.objects.get(name='stop')
        update_data['status'] = stat.id
        await delete_notebook_k8s(authorization, payloads)
        await _notebook.update(**{"ended_at": datetime.datetime.now()})
    else:
        if _notebook.status.name != 'stopped':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')
        stat = await Status.objects.get(name='start')
        update_data['status'] = stat.id
        await create_notebook_k8s(authorization, payloads)
        await _notebook.update(**{"started_at": datetime.datetime.now()})

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
    check, extra_info = await project_check(request, _notebook.project_by_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info)
    if _notebook.status.name not in ['stopped', 'error']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notebook未停止')
    payloads = _notebook.k8s_info
    # error状态调用删除需要释放资源
    if _notebook.status.name == 'error':
        authorization: str = request.headers.get('authorization')
        await delete_notebook_k8s(authorization, payloads)
    await _notebook.delete()


@router_notebook.get(
    '/{notebook_id}/events',
    description='Notebook事件列表',
    response_model=Page[EventItem],
)
async def list_notebook_event(query_params: QueryParameters = Depends(QueryParameters),
                              notebook_id: int = Path(..., ge=1, description="NotebookID")):
    params_filter = query_params.filter_
    events = await Event.find_notebook_events(notebook_id)
    events = await paginate(events.filter(**params_filter), params=query_params.params)
    for i, v in enumerate(events.data):
        events.data[i] = EventItem.parse_obj(v.gen_pagation_event())
    return events


@router_notebook.post(
    '/{notebook_id}/events',
    description='Notebook事件创建',
)
async def create_notebook_event(ec: EventCreate,
                                notebook_id: int = Path(..., ge=1, description="NotebookID")):
    _notebook = await Notebook.objects.select_related(['status']).get(pk=notebook_id)
    d = ec.dict()
    d.update({"status": _notebook.status.desc})
    await Event.objects.create(**d)
    return {}
