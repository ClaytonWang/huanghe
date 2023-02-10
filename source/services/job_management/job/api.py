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
from job.serializers import JobCreate, JobDetail, JobList, JobEdit, JobOp, EventItem
from models import Job, Status, Source
from utils.auth import operate_auth
from utils.k8s_request import create_job_k8s, delete_job_k8s
from utils.storage_request import volume_check
from utils.user_request import get_user_list, get_project_list, project_check
from basic.middleware.account_getter import ADMIN, USER, OWNER
from basic.common.common_model import Event

router_job = APIRouter()


#
# @router_job.get(
#     '/volume/{volume_id}',
#     description='存储-job列表',
# )
# async def get_volume_job(volume_id: int = Path(..., ge=1, description='需要查询的存储 ID')):
#     _job = await Job.objects.all()
#     storage_list = [(x.storage, x.id) for x in _job]
#     volume_note_dict = defaultdict(set)
#     for storage, job_id in storage_list:
#         for x in storage:
#             volume_note_dict[x['storage']['id']].add(job_id)
#     note_ids = volume_note_dict.get(volume_id, [])
#     if not note_ids:
#         return []
#     note_map = {x.id: {"id": x.id, "name": x.name} for x in _job}
#     result = [note_map[x] for x in note_ids]
#     return result


@router_job.get(
    '/{job_id}',
    description="job详情",
    response_model=JobDetail,
    response_model_exclude_unset=True
)
async def get_job(job_id: int = Path(..., ge=1, description='需要查询的job ID')):
    _job = await Job.objects.select_related(
        'status'
    ).get(pk=job_id)
    return _job.gen_job_detail_response()


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
    user: AccountGetter = request.user
    projects = [project.id for project in user.projects]
    if user.role.name == ADMIN:
        jobs = await Job.all_jobs()
    else:
        jobs = await Job.self_projects(projects)
    p = await paginate(jobs.select_related(
        'status'
    ).filter(
        **query_params.filter_
    ), params=query_params.params)
    for i, j in enumerate(p.data):
        p.data[i] = JobList.parse_obj(j.gen_job_pagation_response())
    return p


@router_job.post(
    '',
    description='创建job',
    response_model=JobDetail,
)
async def create_job(request: Request,
                     jc: JobCreate):
    authorization: str = request.headers.get('authorization')
    init_data = {"name": jc.name}
    ag: AccountGetter = request.user
    init_data.update({"created_by_id": ag.id,
                      "updated_by_id": ag.id,
                      "create_en_by": ag.en_name,
                      "created_by": ag.username,
                      "updated_by": ag.username})
    stat = await Status.objects.get(name='stopped')
    init_data['status'] = stat.id

    check, extra_info = await project_check(request, jc.project.id)
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info)
    pg: ProjectGetter = get_project(request.headers.get('authorization'), jc.project.id)
    init_data.update({"project_by_id": pg.id,
                      "project_by": pg.name,
                      "project_en_by": pg.en_name, })

    if await Job.objects.filter(name=init_data['name'], project_by_id=int(jc.project.id)).count():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='job不能重名')

    init_data.update({"mode": jc.mode,
                      "start_command": jc.start_command,
                      "custom": jc.image.custom,
                      "image": jc.image.name,
                      "work_dir": jc.work_dir})

    # 存储检查
    storages, volumes_k8s = await volume_check(authorization, jc.hooks, extra_info)
    path_set = {x['path'] for x in storages}
    if len(path_set) != len(storages):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='目录不能重复')
    init_data['storage'] = json.dumps(storages)

    gpu_count = 0
    if jc.source.startswith("GPU"):
        machine_type = "GPU"
        _, gpu_count, cpu_count, memory = jc.source.split()
        gpu_count = gpu_count.split("*")[0]
        cpu_count = cpu_count.split("C")[0]
        memory = memory.split("G")[0]
    else:
        machine_type = "CPU"
        _, cpu_count, memory = jc.source.split()
        cpu_count = cpu_count.split("C")[0]
        memory = memory.split("G")[0]
    init_data.update({"cpu": cpu_count,
                      "gpu": gpu_count,
                      "memory": memory,
                      "type": machine_type})

    k8s_info = {
        'name': f"{request.user.en_name}-{init_data['name']}",
        'namespace': extra_info,
        'image': jc.image.name,
        'env': get_string_variable('ENV', 'DEV').lower(),
        'cpu': cpu_count,
        'memory': memory,
        'gpu': gpu_count,
        'type': machine_type,
        'volumes': volumes_k8s,
    }
    init_data['k8s_info'] = json.dumps(k8s_info)

    _job = await Job.objects.create(**init_data)
    return _job.gen_job_detail_response()


# @router_job.put(
#     '/{job_id}/{status}',
#     description='状态修改',
# )
# async def update_status(request: Request,
#                         job_id: int = Path(..., ge=1, description="JobID"),
#                         status: int = Path(..., ge=1, description="status_id"),
#                         ):
#     _job, reason = await operate_auth(request, job_id)
#     if not _job:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
#
#     if not await _job.update(status=status):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job不存在')
#     return JSONResponse(dict(id=job_id))


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
        if _job.status.name not in ['pending', 'running', 'stop_fail', 'on']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')
        stat = await Status.objects.get(name='stop')
        update_data['status'] = stat.id
        response = await delete_job_k8s(authorization, payloads)
        # if response.status != 200:
        #     _job.status = None
    elif action == 1:
        if _job.status.name not in ['start_fail', 'run_fail', 'stopped']:
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
    # if _job.status.name not in ['stopped', 'error']:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job未停止')

    # payloads = _job.k8s_info
    # # error状态调用删除需要释放资源
    # if _job.status.name == 'error':
    #     authorization: str = request.headers.get('authorization')
    #     response = await delete_job_k8s(authorization, payloads)
    # if response.status != 200:
    #     _job.status = None
    await _job.delete()


@router_job.get(
    '/{job_id}/events',
    description='Job事件列表',
    response_model=Page[EventItem],
)
async def list_job_event(query_params: QueryParameters = Depends(QueryParameters),
                              job_id: int = Path(..., ge=1, description="JobID")):
    params_filter = query_params.filter_
    # events = await Event.find_notebook_events(notebook_id)
    events = await paginate(Event.objects.filter(**params_filter), params=query_params.params)
    for i, v in enumerate(events.data):
        events.data[i] = EventItem.parse_obj(v.gen_pagation_event())
    return events