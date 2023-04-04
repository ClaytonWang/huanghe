# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/14 15:49
"""
from fastapi import APIRouter

from services.cluster.k8s.cluster_client import cc
from services.cluster.namespace_pipeline.serializers import NamespacePipeline, Namespace
from basic.middleware.rsp import success_common_response

router_namespace_pipeline = APIRouter()


@router_namespace_pipeline.post(
    '',
    description='创建namespace & network',
)
def create_namespace_pipeline(np: NamespacePipeline):
    cc.create_namespace_pipeline(np)
    return success_common_response()



@router_namespace_pipeline.delete(
    '',
    description='删除namespace & network',
)
def delete_service(ns: Namespace):
    cc.delete_namespace_pipeline(ns)
    return success_common_response()
