from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from pvc.serializers import PVC
from k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response


router_pvc = APIRouter()


@router_pvc.post(
    '',
    description='创建存储卷',
)
def create_pvc(pvc: PVC):
    cc.create_namespaced_persistent_volume_claim(pvc)
    return success_common_response()
#
# @router_pvc.delete(
#     '',
#     description='删除存储卷',
#     response_model=PVC,x
# )
# def delete_namespace(pvc: PVC):
#     cc.delete_namespace(pvc)
#     return pvc