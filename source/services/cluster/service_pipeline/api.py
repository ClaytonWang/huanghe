# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/14 15:49
"""
from fastapi import APIRouter

from services.cluster.k8s.cluster_client import cc
from services.cluster.service_pipeline.serializers import ServicePipelineCreateReq, ServicePipeline, ServicePipelineDeleteReq
from basic.middleware.rsp import success_common_response

router_service_pipeline = APIRouter()


@router_service_pipeline.post(
    '',
    description='创建service && deployments && ingress',
)
def create_service_pipeline(spcr: ServicePipelineCreateReq):
    cc.create_service_pipeline(ServicePipeline.parse_obj(spcr.gen_service_pipeline_dict()))
    return success_common_response()


@router_service_pipeline.delete(
    '',
    description='删除service',
)
def delete_service(spdr: ServicePipelineDeleteReq):
    cc.delete_service_pipeline(spdr)
    return success_common_response()
