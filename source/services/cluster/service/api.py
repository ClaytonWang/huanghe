# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/14 15:49
"""
from fastapi import APIRouter

from services.cluster.k8s.cluster_client import cc, hwc
from services.cluster.service.serializers import ServiceCreateReq, Service, ServiceDeleteReq, ServiceQuery
from basic.middleware.rsp import success_common_response

router_service = APIRouter()


@router_service.post(
    '',
    description='创建service',
)
def create_service(servcr: ServiceCreateReq):
    cc.create_service(Service.parse_obj(servcr.gen_service_dict()))
    return success_common_response()


@router_service.post(
    '/batch',
    description='批量查询service',
)
def list_service(servq: ServiceQuery):
    # for test to diff env
    env = servq.env
    if env == 'huawei':
        return hwc.list_service(servq)
    else:
        return cc.list_service(servq)


@router_service.delete(
    '',
    description='删除service',
)
def delete_service(serv: ServiceDeleteReq):
    cc.delete_service(serv)
    return success_common_response()
