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
from basic.utils.source import source_convert
from basic.common.query_filter_params import QueryParameters
from basic.middleware.account_getter import AccountGetter, ProjectGetter, get_project, create_vcjob, \
    delete_vcjob, VolcanoJobCreateReq, VolcanoJobDeleteReq
from services.job_management.job.dependencies import verify_project_check, verify_auth, verify_action, \
    verify_edit_same_job, \
    verify_status_name, verify_create_same_job
from services.job_management.job.serializers import JobCreate, JobDetail, JobList, JobEdit, \
    EventItem, EventCreate, JobStatusUpdate, JobSimple
from services.job_management.models.job import Job
from services.job_management.models.mode import Mode
from basic.middleware.service_requests import volume_check
from basic.common.base_config import ADMIN, ENV
from basic.common.event_model import Event
from basic.common.status_cache import sc

router_job = APIRouter()


@router_job.get(
    '/startmodes',
    description="任务启动方式"
)
async def list_modes():
    return await Mode.mode_cache_pagation()

@router_job.get(
    '/project_backend/{project_id}',
    description='通过项目查询job',
)
async def list_job_by_project(project_id: int = Path(..., ge=1, description='需要查询项目的project id'),
                              user_id: int = Query(None, description='用户id')) -> bool:
    if user_id:
        jc = await Job.self_project_and_self_view(project_id=project_id, self_id=user_id)
    else:
        jc = await Job.self_project(project_id)
    if not jc:
        return False
    return True


@router_job.get(
    '/by_server/{server_ip}',
    description='通过节点IP查询job',
)
async def list_nb_by_server(server_ip: str = Path(..., description='需要查询项目的server_ip')):
    return await Job.project_list_by_ip(server_ip)


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

    if user.role.name == ADMIN:
        jobs = await Job.all_jobs()
    else:
        jobs = await Job.self_view(user.id)

    query = await jobs.select_related('status').filter(**params_filter).all()
    # print(query)
    res = [x.gen_job_simple_response() for x in query]
    # print(res)
    return res


@router_job.get(
    '/{job_id}',
    description="job详情",
    response_model=JobDetail,
    response_model_exclude_unset=True
)
async def get_job(job_id: int = Path(..., ge=1, description='需要查询的job ID')):
    _job = await Job.objects.select_related(
        ['status', "start_mode"]
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
    if user.role.name == ADMIN:
        jobs = await Job.all_jobs()
    else:
        jobs = await Job.self_view(user.id)
    p = await paginate(jobs.select_related(
        'status'
    ).order_by(Job.updated_at.desc()).filter(
        **query_params.filter_
    ), params=query_params.params)
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
    if len(set(x['path'] for x in storages)) != len(storages):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='目录不能重复')

    machine_type, gpu_count, cpu_count, memory = source_convert(jc.source)

    k8s_info = VolcanoJobCreateReq(name=f"{ag.en_name}-{jc.name}",
                                   namespace=pg.en_name,
                                   image=jc.image.name,
                                   env=ENV,
                                   cpu=cpu_count,
                                   memory=memory,
                                   gpu=gpu_count,
                                   volumes=volumes_k8s,
                                   command=[jc.start_command],
                                   working_dir=jc.work_dir, ).dict()

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
                 "start_mode": jc.start_mode,
                 "nodes": jc.nodes,
                 }

    _job = await Job.objects.create(**init_data)
    k8s_info['annotations'] = {"id": str(_job.id)}
    await _job.update(**{"k8s_info": k8s_info})
    return _job.gen_job_detail_response()


@router_job.put(
    '/{job_id}/status_update',
    description='状态更新',
)
async def update_status(jsu: JobStatusUpdate,
                        job_id: int = Path(..., ge=1, description="JobID")):
    j = await Job.get_job_related_status_by_pk(job_id)
    if not j:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job不存在")
    st = Job.compare_status_and_update(jsu.status, sc)
    update_data = {"status": st}
    if jsu.status in {"Failed", "Completed", "Terminated"}:
        update_data.update({"ended_at": datetime.datetime.now()})
    if jsu.server_ip:
        update_data['server_ip'] = jsu.server_ip
    await j.update(**update_data)
    return JSONResponse(dict(id=job_id))


@router_job.put(
    '/{job_id}',
    description='编辑Job',
    dependencies=[Depends(verify_edit_same_job), Depends(verify_status_name)]
)
async def update_job(request: Request,
                     je: JobEdit,
                     job_id: int = Path(..., ge=1, description="JobID"),
                     _job: Job = Depends(verify_auth),
                     extra_info: dict = Depends(verify_project_check)
                     ):
    authorization: str = request.headers.get('authorization')
    if je.mode == "调试":
        je.start_command = "sleep 14400"

    k8s_info = _job.k8s_info

    if _job.status.name != 'stopped':
        delete_vcjob(vjd=VolcanoJobDeleteReq.parse_obj(k8s_info), ignore_no_found=True)

    update_data = {}
    if je.source:
        machine_type, gpu_count, cpu_count, memory = source_convert(je.source)
        source_dic = {'cpu': cpu_count,
                      'memory': memory,
                      'gpu': gpu_count,
                      'type': machine_type, }
        k8s_info.update(source_dic)
        update_data = source_dic

    storages, volumes_k8s = await volume_check(authorization, je.hooks, extra_info['en_name'])
    if len(set(x['path'] for x in storages)) != len(storages):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='目录不能重复')
    k8s_info.update({"volumes": volumes_k8s,
                     'image': je.image.name,
                     'namespace': extra_info['en_name'],
                     'name': f"{request.user.en_name}-{_job.name}",
                     "command": [je.start_command],
                     "work_dir": je.work_dir,
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
                        "start_mode": je.start_mode,
                        "nodes": je.nodes,
                        })
    if not await _job.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job不存在')
    return JSONResponse(dict(id=job_id))


@router_job.post(
    '/{job_id}',
    description='启动/停止Job',
)
async def operate_job(job_id: int = Path(..., ge=1, description="JobID"),
                      _job: Job = Depends(verify_auth),
                      action: int = Depends(verify_action)):
    payloads = json.dumps(_job.k8s_info)

    # 数字，0（停止）｜1（启动）
    update_data = {}
    if action == 0:
        update_data['status'] = sc.get('stopped')
        delete_vcjob(vjd=VolcanoJobDeleteReq.parse_raw(payloads), ignore_no_found=True)
        await _job.update(**{"ended_at": datetime.datetime.now()})
    elif action == 1:
        update_data['status'] = sc.get('pending')
        create_vcjob(vjc=VolcanoJobCreateReq.parse_raw(payloads))
        await _job.update(**{"started_at": datetime.datetime.now()})

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新数据不能为空')
    if not await _job.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job不存在')
    return JSONResponse(dict(id=job_id))



@router_job.delete(
    '/{job_id}',
    description='删除Job',
    dependencies=[Depends(verify_project_check)]
)
async def delete_job(_job: Job = Depends(verify_auth)):

    payloads = _job.k8s_info
    # # error状态调用删除需要释放资源
    if _job.status.name != 'stop':
        delete_vcjob(vjd=VolcanoJobDeleteReq.parse_obj(dict(payloads)), ignore_no_found=True)
    await _job.delete()


@router_job.get(
    '/{job_id}/events',
    description='Job事件列表',
    response_model=Page[EventItem],
)
async def list_job_event(query_params: QueryParameters = Depends(QueryParameters),
                         job_id: int = Path(..., ge=1, description="JobID")):
    params_filter = query_params.filter_
    events = await Event.find_vcjob_events(job_id)
    events = await paginate(events.filter(**params_filter), params=query_params.params)
    for i, v in enumerate(events.data):
        events.data[i] = EventItem.parse_obj(v.gen_pagation_event())
    return events


@router_job.post(
    '/{job_id}/events',
    description='Job事件创建',
)
async def create_notebook_event(ec: EventCreate,
                                job_id: int = Path(..., ge=1, description="JobID")):
    j = await Job.objects.select_related(['status']).get(pk=job_id)
    d = ec.dict()
    d.update({"status": j.status.desc})
    await Event.objects.create(**d)
    return {}
