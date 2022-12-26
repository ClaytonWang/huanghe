from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from namespace.serializers import Namespace
from k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response
from kubernetes.client import ApiException

router_namespace = APIRouter()


@router_namespace.post(
    '',
    description='创建命名空间',
)
def create_namespace(ns: Namespace):
    cc.create_namespace(ns)
    return success_common_response()

@router_namespace.delete(
    '',
    description='删除命名空间',
    response_model=Namespace,
)
def delete_namespace(ns: Namespace):
    cc.delete_namespace(ns)
    return success_common_response()