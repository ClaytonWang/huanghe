from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from namespace.serializers import Namespace
from k8s.cluster_client import cc


router_namespace = APIRouter()


@router_namespace.post(
    '',
    description='创建命名空间',
    response_model=Namespace,
)
def create_namespace(ns: Namespace):
    cc.create_namespace(ns)
    return ns

@router_namespace.delete(
    '',
    description='删除命名空间',
    response_model=Namespace,
)
def delete_namespace(ns: Namespace):
    cc.delete_namespace(ns)
    return ns