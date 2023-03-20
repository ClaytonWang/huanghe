# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/16 11:16
"""
import json
from typing import List
from config import *
from basic.utils.source import source_convert
from fastapi import APIRouter, Depends, Request, HTTPException, status, Path, Query
from fastapi.responses import JSONResponse
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from basic.common.event_model import Event
from basic.common.env_variable import get_string_variable
from basic.middleware.account_getter import AccountGetter, ProjectGetter, get_project
from services.cluster.deployment.serializers import Deployment, DeploymentDeleteReq, DeploymentCreateReq, DeploymentListReq
from basic.middleware.service_requests import get_user_list, volume_check
from services.deployment.models.deployment import Deployment

from services.deployment.deployment.serializers import DeploymentList, DeploymentCreate, DeploymentDetail
from services.deployment.utils.auth import operate_auth
from utils.user_request import project_check, project_check_obj
from utils.auth import operate_auth
from collections import defaultdict
from basic.common.base_config import ADMIN, ENV
from basic.common.status_cache import sc
import datetime

router_deployment = APIRouter()

COMMON = "https://grafana.digitalbrain.cn:32443/d-solo/3JLLppA4k/notebookjian-kong?"
ACCOUNT = "jovyan"
PASSWORD = "jovyan"


@router_deployment.get(
    '',
    description='deployment列表',
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
    description='创建deployment',
    response_model=DeploymentDetail,
)
async def create_deployment(request: Request,
                            dc: DeploymentCreate):
    authorization: str = request.headers.get('authorization')
    ag: AccountGetter = request.user
    pg: ProjectGetter = get_project(request.headers.get('authorization'), dc.project.id)

    if await Deployment.objects.filter(name=dc.name, project_by_id=dc.project.id, created_by_id=ag.id).count():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='同一个项目下，同一个用户, deployment不能重名')
    # todo 重名规则待校验

    # 存储检查
    storages, volumes_k8s = await volume_check(authorization, dc.hooks, pg.en_name)
    path_set = {x['path'] for x in storages}
    if len(path_set) != len(storages):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='目录不能重复')

    machine_type, gpu_count, cpu_count, memory = source_convert(dc.source)

    k8s_info = DeploymentCreateReq(name=f"{ag.en_name}-{dc.name}",
                                   namespace=pg.en_name,
                                   image=dc.image.name,
                                   env=ENV,
                                   cpu=cpu_count,
                                   memory=memory,
                                   gpu=gpu_count,
                                   volumes=volumes_k8s,
                                   working_dir=dc.work_dir, ).dict()
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
                 "work_dir": dc.work_dir,
                 "k8s_info": json.dumps(k8s_info),
                 "storage": json.dumps(storages),
                 "cpu": cpu_count,
                 "gpu": gpu_count,
                 "memory": memory,
                 "type": machine_type,
                 "private_ip": dc.private_ip,
                 "public_ip": dc.public_ip,
                 "port": dc.port,
                 }

    _deploy = await Deployment.objects.create(**init_data)
    k8s_info['annotations'] = {"id": str(_deploy.id)}
    await _deploy.update(**{"k8s_info": k8s_info})
    return _deploy.gen_deployment_detail_response()
