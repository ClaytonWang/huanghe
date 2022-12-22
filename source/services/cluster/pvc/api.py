from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from pvc.serializers import PVC
from k8s.cluster_client import cc


router_pvc = APIRouter()


@router_pvc.post(
    '',
    description='创建存储卷',
    response_model=PVC,
)
def create_pvc(pvc: PVC):
    cc.create_namespaced_persistent_volume_claim(pvc)
    return pvc
#
# @router_pvc.delete(
#     '',
#     description='删除存储卷',
#     response_model=PVC,x
# )
# def delete_namespace(pvc: PVC):
#     cc.delete_namespace(pvc)
#     return pvc