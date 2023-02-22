from fastapi import APIRouter
from pvc.serializers import PVCCreateReq, PVCDeleteReq
from k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response


router_pvc = APIRouter()


@router_pvc.post(
    '',
    description='创建存储卷',
)
def create_pvc(pvc: PVCCreateReq):
    cc.create_namespaced_persistent_volume_claim(pvc)
    return success_common_response()

@router_pvc.delete(
    '',
    description='删除存储卷',
)
def delete_pvc(pvc: PVCDeleteReq):
    cc.delete_namespaced_persistent_volume_claim(pvc)
    return success_common_response()