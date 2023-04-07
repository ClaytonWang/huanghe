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

from basic.middleware.service_requests import volume_check
from services.job_management.utils.user_request import project_check_obj
from basic.common.base_config import ADMIN, ENV
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

    _job = await service.save_job(jc=jc, authorization=authorization, ag=ag, pg=pg)

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

    _job = await service.update_job(
        authorization=authorization,
        je=je, _job=_job, k8s_info=k8s_info, extra_info=extra_info,
        username=request.user.en_name
    )
    return _job


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
