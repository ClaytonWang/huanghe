# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/15 10:21
"""
import asyncio
import datetime
import json

from fastapi import APIRouter, Depends, Request, HTTPException, status, Path, Query
from fastapi.responses import JSONResponse

from typing import List
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from basic.middleware.account_getter import AccountGetter, ProjectGetter, get_project, create_vcjob, \
    delete_vcjob, VolcanoJobDeleteReq
from services.job_management.job import service
from services.job_management.job.dependencies import verify_project_check, verify_auth, \
    verify_edit_same_job, verify_status_name, verify_create_same_job, verify_job_related_status
from services.job_management.job.serializers import JobCreate, JobDetail, JobList, JobEditReq, \
    EventItem, EventCreate, JobSimple, JobOpReq, ModeRes, JobStatusUpdateRes, JobStatusUpdateReq, JobEditRes, JobOpRes
from services.job_management.models.job import Job



from services.job_management.utils.auth import operate_auth
from basic.middleware.service_requests import volume_check
from services.job_management.utils.user_request import project_check, project_check_obj
from basic.common.base_config import ADMIN, ENV
from basic.common.event_model import Event
from basic.common.status_cache import sc
from services.job_management.models.mode import Mode
router_job = APIRouter()


@router_job.get(
    '/project_backend/{project_id}',
    description='通过项目查询job',
    response_model=bool
)
async def list_job_by_project(project_id: int = Path(..., ge=1, description='需要查询项目的project id'),
                              user_id: int = Query(None, description='用户id')) -> bool:
    if not await service.count_job_by_project_id(project_id, user_id):
        return False
    return True


@router_job.get(
    '/by_server/{server_ip}',
    description='通过节点IP查询job',
)
async def list_job_by_server(server_ip: str = Path(..., description='需要查询项目的server_ip')):
    return await service.list_project_by_ip(server_ip)


@router_job.get(
    '/items',
    description='job概况',
    response_model=List[JobSimple],
    response_model_exclude_unset=True
)
async def get_simple_job(request: Request,
                         query_params: QueryParameters = Depends(QueryParameters), ):
    params_filter = query_params.filter_
    user: AccountGetter = request.user
    if params_filter:
        if 'creator_id' in params_filter:
            params_filter['created_by_id'] = int(params_filter.pop('creator_id'))
        if 'project_ids' in params_filter:
            project_ids = params_filter.pop('project_ids')
            if isinstance(project_ids, str):
                project_ids = [int(x) for x in project_ids.split(',')]
            params_filter['project_by_id__in'] = project_ids

    return await service.list_simple_job(params_filter=params_filter, user=user)


@router_job.get(
    '/{job_id}',
    description="job详情",
    response_model=JobDetail,
    response_model_exclude_unset=True
)
async def get_job(job_id: int = Path(..., ge=1, description='需要查询的job ID')):
    return await service.get_detail_job_by_id(job_id)


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
    p = await service.list_job(user=user, query_params=query_params)
    for i, j in enumerate(p.data):
        p.data[i] = JobList.parse_obj(j.gen_job_pagation_response())
    return p


@router_job.post(
    '',
    description='创建job',
    response_model=JobDetail,
    dependencies=[Depends(verify_create_same_job)]
)
async def create_job(request: Request,
                     jc: JobCreate):
    authorization: str = request.headers.get('authorization')
    ag: AccountGetter = request.user
    pg: ProjectGetter = get_project(request.headers.get('authorization'), jc.project.id)

    if jc.mode == "调试":
        jc.start_command = "sleep 14400"

    # 存储检查
    storages, volumes_k8s = await volume_check(authorization, jc.hooks, pg.en_name)
    path_set = {x['path'] for x in storages}
    if len(path_set) != len(storages):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='目录不能重复')

    machine_type, gpu_count, cpu_count, memory = source_convert(jc.source)
    start_mode = await Mode.get(jc.start_mode.id)

    k8s_info = VolcanoJobCreateReq(name=f"{ag.en_name}-{jc.name}",
                                   namespace=pg.en_name,
                                   image=jc.image.name,
                                   env=ENV,
                                   cpu=cpu_count,
                                   memory=memory,
                                   gpu=gpu_count,
                                   volumes=volumes_k8s,
                                   command=[jc.start_command],
                                   working_dir=jc.work_dir,
                                   task_num=jc.nodes,
                                   mode=start_mode,).dict()

    init_data = {"name": jc.name,
                 "created_by_id": ag.id,
                 "updated_by_id": ag.id,
                 "create_en_by": ag.en_name,
                 "created_by": ag.username,
                 "updated_by": ag.username,
                 "status": sc.get('stopped'),
                 "project_by_id": pg.id,
                 "project_by": pg.name,
                 "project_en_by": pg.en_name,
                 "mode": jc.mode,
                 "start_command": jc.start_command,
                 "custom": jc.image.custom,
                 "image": jc.image.name,
                 "work_dir": jc.work_dir,
                 "k8s_info": json.dumps(k8s_info),
                 "storage": json.dumps(storages),
                 "cpu": cpu_count,
                 "gpu": gpu_count,
                 "memory": memory,
                 "type": machine_type,
                 "start_mode": jc.start_mode.id,
                 "nodes": jc.nodes,
                 }

    _job = await Job.objects.create(**init_data)
    k8s_info['annotations'] = {"id": str(_job.id), "gpu": str(gpu_count), "slots": str(gpu_count) if gpu_count else "1"}
    await _job.update(**{"k8s_info": k8s_info})
    return _job.gen_job_detail_response()


@router_job.put(
    '/{job_id}/status_update',
    description='状态更新',
    response_model=JobStatusUpdateRes
)
async def update_status(jsu: JobStatusUpdateReq,
                        _job: Job = Depends(verify_job_related_status)):
    _job = await service.update_status(jsu_status=jsu.status, jsu_server_ip=jsu.server_ip, job=_job)
    return _job


@router_job.put(
    '/{job_id}',
    description='编辑Job',
    dependencies=[Depends(verify_edit_same_job), Depends(verify_status_name)],
    response_model=JobEditRes
)
async def update_job(request: Request,
                     je: JobEditReq,
                     _job: Job = Depends(verify_auth),
                     extra_info: dict = Depends(verify_project_check)
                     ):
    authorization: str = request.headers.get('authorization')
    if je.mode == "调试":
        je.start_command = "sleep 14400"

    k8s_info = _job.k8s_info

    if _job.status.name != 'stopped':
        delete_vcjob(vjd=VolcanoJobDeleteReq.parse_obj(k8s_info), ignore_no_found=True)

    check, extra_info = await project_check_obj(request, je.project.id)
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info)

    update_data = {}
    start_mode = await Mode.get(je.start_mode.id)

    if je.source:
        machine_type, gpu_count, cpu_count, memory = source_convert(je.source)
        source_dic = {'cpu': cpu_count,
                      'memory': memory,
                      'gpu': gpu_count,
                      'type': machine_type,
                      }
        k8s_info.update(source_dic)
        k8s_info['annotations'] = {"id": str(_job.id), "gpu": str(gpu_count), "slots": str(gpu_count) if gpu_count else "1"}
        update_data = source_dic

    storages, volumes_k8s = await volume_check(authorization, je.hooks, extra_info['en_name'])
    path_set = {x['path'] for x in storages}
    if len(path_set) != len(storages):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='目录不能重复')
    k8s_info.update({"volumes": volumes_k8s,
                     'image': je.image.name,
                     'namespace': extra_info['en_name'],
                     'name': f"{request.user.en_name}-{_job.name}",
                     "command": [je.start_command],
                     "work_dir": je.work_dir,
                     "task_num": je.nodes,
                     "mode": start_mode,
                     })
    update_data.update({"storage": json.dumps(storages),
                        "k8s_info": json.dumps(k8s_info),
                        "updated_at": datetime.datetime.now(),
                        "project_by_id": je.project.id,
                        "project_by": extra_info['name'],
                        "image": je.image.name,
                        "custom": je.image.custom,
                        "work_dir": je.work_dir,
                        'status': sc.get('stopped'),
                        "mode": je.mode,
                        "start_command": je.start_command,
                        "start_mode": je.start_mode.id,
                        "nodes": je.nodes,
                        })
    if not await _job.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job不存在')
    return JSONResponse(dict(id=job_id))


@router_job.post(
    '/{job_id}',
    description='启动/停止Job',
    response_model=JobOpRes
)
async def operate_job(job_op: JobOpReq,
                      _job: Job = Depends(verify_auth)):
    payloads = json.dumps(_job.k8s_info)

    _job = await service.update_job_by_operate(job_op=job_op, payloads=payloads, _job=_job)
    return _job


@router_job.delete(
    '/{job_id}',
    description='删除Job',
    dependencies=[Depends(verify_project_check)]
)
async def delete_job(_job: Job = Depends(verify_auth)):
    await service.delete_job(_job=_job)


@router_job.get(
    '/{job_id}/events',
    description='Job事件列表',
    response_model=Page[EventItem],
)
async def list_job_event(query_params: QueryParameters = Depends(QueryParameters),
                         job_id: int = Path(..., ge=1, description="JobID")):
    return await service.list_job_event(job_id=job_id, query_params=query_params)


@router_job.post(
    '/{job_id}/events',
    description='Job事件创建',
)
async def create_job_event(ec: EventCreate,
                           job_id: int = Path(..., ge=1, description="JobID")):
    await service.save_job_event(ec=ec, job_id=job_id)
    return {}
