# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/14 15:49
"""
from fastapi import APIRouter

from services.cluster.k8s.cluster_client import cc
from services.cluster.service_pipeline.serializers import ServiceCreateReq, Service, ServiceDeleteReq, ServiceQuery
from basic.middleware.rsp import success_common_response

router_service_pipeline = APIRouter()


@router_service_pipeline.post(
    '',
    description='创建service pipeline',
)
def create_service(servcr: ServiceCreateReq):
    #TODO(jiangshouchen): create service/ingress/deployments
    cc.create
    return success_common_response()


@router_service_pipeline.post(
    '/batch',
    description='批量查询service',
)
def list_service(servq: ServiceQuery):
    return cc.list_service(servq)


@router_service_pipeline.delete(
    '',
    description='删除service',
)
def delete_service(serv: ServiceDeleteReq):
    cc.delete_service(serv)
    return success_common_response()
