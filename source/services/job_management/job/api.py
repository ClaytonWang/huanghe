# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/15 10:21
"""
import datetime
import json
from collections import defaultdict

from fastapi import APIRouter, Depends, Request, HTTPException, status, Path
from fastapi.responses import JSONResponse

from basic.common.env_variable import get_string_variable
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from basic.middleware.account_getter import AccountGetter, ProjectGetter, get_project
from job.serializers import JobCreate, JobDetail, JobList, JobEdit, JobOp
from models import Job, Status, Source
from utils.auth import operate_auth
from utils.k8s_request import create_job_k8s, delete_job_k8s
from utils.storage_request import volume_check
from utils.user_request import get_user_list, get_project_list, project_check

router_job = APIRouter()


def format_job_detail(nb: Job, source: Source = None):
    result = nb.dict()
    if source:
        result['source'] = source.get_str()
    result['project'] = {"id": nb.project_by_id,
                         "name": nb.project_by, }

    result['image'] = {"desc": "",
                       "name": nb.image_name,
                       "custom": nb.image_type, }
    result['creator'] = {"id": nb.created_by_id,
                         "username": nb.created_by, }
    result['hooks'] = result['storage']
    result['task_model_name'] = nb.get_task_model_name()
    return result


@router_job.get(
    '/volume/{volume_id}',
    description='存储-job列表',
)
async def get_volume_job(volume_id: int = Path(..., ge=1, description='需要查询的存储 ID')):
    _job = await Job.objects.all()
    storage_list = [(x.storage, x.id) for x in _job]
    volume_note_dict = defaultdict(set)
    for storage, job_id in storage_list:
        for x in storage:
            volume_note_dict[x['storage']['id']].add(job_id)
    note_ids = volume_note_dict.get(volume_id, [])
    if not note_ids:
        return []
    note_map = {x.id: {"id": x.id, "name": x.name} for x in _job}
    result = [note_map[x] for x in note_ids]
    return result


@router_job.get(
    '/{job_id}',
    description="job详情",
    response_model=JobDetail,
    response_model_exclude_unset=True
)
async def get_job(job_id: int = Path(..., ge=1, description='需要查询的job ID')):
    _job = await Job.objects.select_related(['status']).get(pk=job_id)
    source = await Source.objects.get(pk=_job.source_id)
    return format_job_detail(_job, source)


@router_job.get(
    '',
    description='job列表',
    response_model=Page[JobList],
    response_model_exclude_unset=True
)
async def list_job(request: Request,
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
    # code_id_map = {x['code']: x['id'] for x in project_list}
    res_proj_map = {x['id']: {'id': x['id'], 'name': x['name']} for x in project_list}

    # 用户可见项目
    if role_name != 'admin':
        viewable_project_ids = id_proj_map.get(request.user.id)
        params_filter['project_by_id__in'] = viewable_project_ids
        params_filter['created_by_id'] = request.user.id

    if params_filter:
        name_filter, role_filter, need_filter = {}, {}, False
        if 'username' in params_filter:
            name = params_filter.pop('username')
            # name_filter = set(name_userid_map.get(name, []))
            # need_filter = True
        if 'project__code' in params_filter:
            project_code = params_filter.pop('project__code')
            # params_filter['project_id'] = code_id_map.get(project_code)
        if 'role__name' in params_filter:
            role__name = params_filter.pop('role__name')
            # role_filter = set(role_userid_map.get(role__name, []))
            # need_filter = True
        # if name_filter and role_filter:
        #     params_filter['creator_id__in'] = list(name_filter.intersection(role_filter))
        # elif need_filter:
        #     params_filter['creator_id__in'] = list(name_filter or role_filter)
    # todo 要修改合理的params_filter，不然会报错
    # print("show filter")
    # print(params_filter)

    result = await paginate(Job.objects.select_related(
        ['status']
    ).filter(**params_filter), params=query_params.params)
    result = result.dict()
    data = result['data']

    source_ids = (item['source_id'] for item in data)
    source_list = await Source.objects.filter(id__in=source_ids).all()
    source_list_map = {source.id: source for source in source_list}
    for item in data:
        source = source_list_map.get(item['source_id'])
        gpu = source.gpu
        type = source.type
        cpu = source.cpu
        memory = source.memory
        if gpu:
            item['source'] = f"GPU {gpu}*{type} {cpu}C {memory}G"
        else:
            item['source'] = f"CPU {cpu}C {memory}G"

        item['creator'] = {
            "id": item["created_by_id"],
            "username": item["created_by"],
        }
        item['image'] = {
            'name': item['image_name'],
            'desc': "",
            "custom": item['image_type'],
        }

        project_id = item.pop('project_by_id')
        project_info = res_proj_map.get(project_id)
        item['project'] = project_info
        task_model = item['task_model']
        if task_model == 0:
            item['task_model_name'] = "调试"
        if task_model == 1:
            item['task_model_name'] = "非调试"
    return result


@router_job.post(
    '',
    description='创建job',
    response_model=JobDetail,
)
async def create_job(request: Request,
                     nc: JobCreate):
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

    if await Job.objects.filter(name=init_data['name'], project_by_id=int(nc.project.id)).count():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='job不能重名')

    init_data['source_id'] = nc.source_id
    init_data['task_model'] = nc.task_model
    init_data['start_command'] = nc.start_command
    init_data['image_type'] = nc.image_type
    init_data['image_name'] = nc.image_name
    init_data['work_dir'] = nc.work_dir

    # 存储检查
    storages, volumes_k8s = await volume_check(authorization, nc.hooks, extra_info)
    path_set = {x['path'] for x in storages}
    if len(path_set) != len(storages):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='目录不能重复')
    init_data['storage'] = json.dumps(storages)

    source = await Source.objects.get(pk=nc.source_id)
    k8s_info = {
        'name': f"{request.user.en_name}-{init_data['name']}",
        'namespace': extra_info,
        'image': nc.image_name,
        'env': get_string_variable('ENV', 'DEV').lower(),
        'cpu': source.cpu,
        'memory': source.memory,
        'gpu': source.gpu,
        'type': source.type,
        'volumes': volumes_k8s,
    }
    init_data['k8s_info'] = json.dumps(k8s_info)

    _job = await Job.objects.create(**init_data)
    return format_job_detail(_job)


@router_job.put(
    '/{job_id}/{status}',
    description='状态修改',
)
async def update_status(request: Request,
                        job_id: int = Path(..., ge=1, description="JobID"),
                        status: int = Path(..., ge=1, description="status_id"),
                        ):
    _job, reason = await operate_auth(request, job_id)
    if not _job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

    if not await _job.update(status=status):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job不存在')
    return JSONResponse(dict(id=job_id))


@router_job.put(
    '/{job_id}',
    description='编辑Job',
)
async def update_job(request: Request,
                     ne: JobEdit,
                     job_id: int = Path(..., ge=1, description="JobID"),
                     ):
    # user: AccountGetter = request.user
    authorization: str = request.headers.get('authorization')
    update_data = ne.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新数据不能为空')

    _job, reason = await operate_auth(request, job_id)
    if not _job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    k8s_info = _job.k8s_info

    if _job.status.name != 'stopped':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job未停止')

    project_id = ne.project.id
    check, extra_info = await project_check(request, project_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info)
    update_data['project_by_id'] = project_id
    if 'project' in update_data:
        update_data.pop('project')
    k8s_info['namespace'] = extra_info

    k8s_info['name'] = f"{request.user.en_name}-{_job.name}"

    if ne.source_id:
        source = await Source.objects.get(pk=ne.source_id)
        k8s_info.update({
            'cpu': source.cpu,
            'memory': source.memory,
            'gpu': source.gpu,
            'type': source.type,
        })

    k8s_info['image'] = ne.image_name

    update_data.pop('hooks')
    storages, volumes_k8s = await volume_check(authorization, ne.hooks, extra_info)
    path_set = {x['path'] for x in storages}
    if len(path_set) != len(storages):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='目录不能重复')
    update_data['storage'] = json.dumps(storages)
    k8s_info['volumes'] = volumes_k8s

    update_data['k8s_info'] = json.dumps(k8s_info)
    update_data['updated_at'] = datetime.datetime.now()
    if not await _job.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job不存在')
    return JSONResponse(dict(id=job_id))


@router_job.post(
    '/{job_id}',
    description='启动/停止Job',
)
async def operate_job(request: Request,
                      data: JobOp,
                      job_id: int = Path(..., ge=1, description="JobID")):
    authorization: str = request.headers.get('authorization')
    action = int(data.dict()['action'])
    _job, reason = await operate_auth(request, job_id)
    if not _job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    if action not in [0, 1]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')
    payloads = json.dumps(_job.k8s_info)

    # 数字，0（停止）｜1（启动）
    # todo 状态还需要调整
    update_data = {}
    if action == 0:
        if _job.status.name not in ['pending', 'running', 'stop_fail','on']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')
        stat = await Status.objects.get(name='stop')
        update_data['status'] = stat.id
        response = await delete_job_k8s(authorization, payloads)
        # if response.status != 200:
        #     _job.status = None
    elif action==1:
        if _job.status.name not in ['start_fail','run_fail','stopped']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')
        stat = await Status.objects.get(name='pending')
        update_data['status'] = stat.id
        # todo response返回不为200时更新job状态到异常
        response = await create_job_k8s(authorization, payloads)
        # if response.status != 200:
        #     _job.status = None
    # print(response)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新数据不能为空')
    if not await _job.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job不存在')
    return JSONResponse(dict(id=job_id))


@router_job.delete(
    '/{job_id}',
    description='删除Job',
)
async def delete_job(request: Request,
                     job_id: int = Path(..., ge=1, description="JobID")):
    _job, reason = await operate_auth(request, job_id)
    if not _job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    check, extra_info = await project_check(request, _job.project_by_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info)
    if _job.status.name not in ['stopped', 'error']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job未停止')

    payloads = _job.k8s_info
    # error状态调用删除需要释放资源
    if _job.status.name == 'error':
        authorization: str = request.headers.get('authorization')
        response = await delete_job_k8s(authorization, payloads)
        # if response.status != 200:
        #     _job.status = None
    await _job.delete()
