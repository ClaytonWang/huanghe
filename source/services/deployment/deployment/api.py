# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/16 11:16
"""
import json
from config import *
from basic.utils.source import source_convert
from fastapi import APIRouter, Depends, Request, HTTPException, status, Path
from fastapi.responses import JSONResponse
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from basic.middleware.account_getter import AccountGetter, ProjectGetter, get_project
from basic.middleware.service_requests import get_user_list, volume_check

from services.deployment.deployment.serializers import DeploymentList, DeploymentCreate, DeploymentDetail, \
    DeploymentEdit, DeploymentOp, DeploymentStatusUpdate, DeploymentDeleteReq, DeploymentCreateReq, \
    DeploymentListReq, DeploymentItem
from services.deployment.models.deployment import Deployment
from services.deployment.utils.auth import operate_auth
from services.deployment.utils.k8s_request import create_deploy_k8s_pipeline, delete_deploy_k8s_pipeline
from utils.user_request import project_check, project_check_obj
from utils.auth import operate_auth
from basic.common.base_config import ADMIN, ENV
from basic.common.status_cache import sc
import datetime

router_deployment = APIRouter()



@router_deployment.get(
    '/{deployment_id}',
    description="Deployment详情",
    response_model=DeploymentDetail,
    response_model_exclude_unset=True
)
async def get_deployment(deployment_id: int = Path(..., ge=1, description='需要查询的deployment ID')):
    _deployment = await Deployment.objects.select_related(['status']).get(pk=deployment_id)
    return _deployment.gen_deployment_detail_response()


@router_deployment.get(
    '',
    description='Deployment列表',
    response_model=Page[DeploymentList],
    response_model_exclude_unset=True
)
async def list_deployment(request: Request,
                          query_params: QueryParameters = Depends(QueryParameters),
                          ):
    """
    :param request:
    :param query_params:
    :return:
    """
    user: AccountGetter = request.user
    if user.role.name == ADMIN:
        deploys = await Deployment.all_deployments()
    else:
        deploys = await Deployment.self_view(user.id)
    p = await paginate(deploys.select_related(
        'status'
    ).order_by(Deployment.updated_at.desc()).filter(
        **query_params.filter_
    ), params=query_params.params)
    for i, j in enumerate(p.data):
        p.data[i] = DeploymentList.parse_obj(j.gen_deployment_pagation_response())
    return p


@router_deployment.post(
    '',
    description='创建Deployment',
    response_model=DeploymentDetail,
)
async def create_deployment(request: Request,
                            dc: DeploymentCreate):
    authorization: str = request.headers.get('authorization')
    ag: AccountGetter = request.user
    pg: ProjectGetter = get_project(request.headers.get('authorization'), dc.project.id)

    if await Deployment.objects.filter(name=dc.name, project_by_id=dc.project.id, created_by_id=ag.id).count():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='同一个项目下，同一个用户, Deployment不能重名')

    machine_type, gpu_count, cpu_count, memory = source_convert(dc.source)

    # k8s_info = DeploymentCreateReq(name=f"{ag.en_name}-{dc.name}",
    #                                namespace=pg.en_name,
    #                                image=dc.image.name,
    #                                env=ENV,
    #                                cpu=cpu_count,
    #                                memory=memory,
    #                                gpu=gpu_count,
    #                                working_dir=dc.work_dir, ).dict()
    # TODO 要加上创建路由等的

    init_data = {"name": dc.name,
                 "created_by_id": ag.id,
                 "updated_by_id": ag.id,
                 "create_en_by": ag.en_name,
                 "created_by": ag.username,
                 "updated_by": ag.username,
                 "status": sc.get('stopped'),
                 "project_by_id": pg.id,
                 "project_by": pg.name,
                 "project_en_by": pg.en_name,
                 "custom": dc.image.custom,
                 "image": dc.image.name,
                 "cpu": cpu_count,
                 "gpu": gpu_count,
                 "memory": memory,
                 "type": machine_type,
                 # "private_ip": dc.private_ip,
                 # "public_ip": dc.public_ip,
                 # "port": dc.port,
                 # "private_ip": "待连接service",
                 # "public_ip": "待连接service",
                 # "port": 80,
                 }

    _deploy = await Deployment.objects.create(**init_data)
    # k8s_info['annotations'] = {"id": str(_deploy.id)}
    # await _deploy.update(**{"k8s_info": k8s_info})
    return _deploy.gen_deployment_detail_response()



@router_deployment.put(
    '/{deployment_id}',
    description='编辑Deployment',
)
async def update_deployment(request: Request,
                            de: DeploymentEdit,
                            deployment_id: int = Path(..., ge=1, description="DeploymentID"),
                            ):
    ag: AccountGetter = request.user
    authorization: str = request.headers.get('authorization')

    _deploy, reason = await operate_auth(request, deployment_id)
    if not _deploy:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

    duplicate_name = await Deployment.objects.filter(name=_deploy.name, project_by_id=int(de.project.id),
                                                     created_by_id=ag.id).exclude(id=deployment_id).count()
    if duplicate_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='同一个项目下，同一个用户，Deployment不能重名')
    k8s_info = _deploy.k8s_info

    if _deploy.status.name not in {'stopped', "completed", "run_fail"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Deployment未停止')
    if _deploy.status.name != 'stopped':
        delete_deploy_k8s_pipeline(json.dumps(k8s_info), ignore_no_found=True)

    check, extra_info = await project_check_obj(request, de.project.id)
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info)

    update_data = {}
    if de.source:
        machine_type, gpu_count, cpu_count, memory = source_convert(de.source)
        source_dic = {'cpu': cpu_count,
                      'memory': memory,
                      'gpu': gpu_count,
                      'type': machine_type, }
        k8s_info.update(source_dic)
        update_data = source_dic


    update_data.update({"updated_at": datetime.datetime.now(),
                        "project_by_id": de.project.id,
                        "project_by": extra_info['name'],
                        "image": de.image.name,
                        "custom": de.image.custom,
                        "work_dir": de.work_dir,
                        'status': sc.get('stopped'),
                        })
    if not await _deploy.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Deployment不存在')
    return JSONResponse(dict(id=deployment_id))


@router_deployment.post(
    '/{deployment_id}',
    description='启动/停止Deployment',
)
async def operate_deployment(request: Request,
                             data: DeploymentOp,
                             deployment_id: int = Path(..., ge=1, description="DeploymentID")):
    action = int(data.dict()['action'])
    _deploy, reason = await operate_auth(request, deployment_id)
    if not _deploy:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    if action not in [0, 1]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')
    payloads = json.dumps(_deploy.k8s_info)

    # 数字，0（停止）｜1（启动）
    update_data = {}
    if action == 0:
        update_data['status'] = sc.get('stopped')
        delete_deploy_k8s_pipeline(payloads, ignore_no_found=True)
        await _deploy.update(**{"ended_at": datetime.datetime.now()})
    elif action == 1:
        update_data['status'] = sc.get('pending')
        create_deploy_k8s_pipeline(payloads)
        await _deploy.update(**{"started_at": datetime.datetime.now()})

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新数据不能为空')
    if not await _deploy.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Deployment不存在')
    return JSONResponse(dict(id=deployment_id))


@router_deployment.delete(
    '/{deployment_id}',
    description='删除Deployment',
)
async def delete_deployment(request: Request,
                            deployment_id: int = Path(..., ge=1, description="DeploymentID")):
    _deploy, reason = await operate_auth(request, deployment_id)
    if not _deploy:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    check, extra_info = await project_check(request, _deploy.project_by_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info)

    payloads = _deploy.k8s_info
    # # error状态调用删除需要释放资源
    if _deploy.status.name != 'stop':
        delete_deploy_k8s_pipeline(json.dumps(payloads), ignore_no_found=True)
    await _deploy.delete()
