from fastapi import APIRouter
from services.cluster.namespace.serializers import Namespace
from services.cluster.k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response

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
