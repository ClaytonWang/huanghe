from fastapi import APIRouter
from services.cluster.pod.serializers import Pod
from services.cluster.k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response

router_pod = APIRouter()


@router_pod.post(
    '',
    description='创建存储卷',
)
def read_pod_log(p: Pod):
    cc.read_namespaced_pod_log(p)
    return success_common_response()
