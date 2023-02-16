from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from pod.serializers import Pod
from k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response


router_pod = APIRouter()


@router_pod.post(
    '',
    description='创建存储卷',
)
def read_pod_log(p: Pod):
    res = cc.read_namespaced_pod_log(p)
    print(res)
    return success_common_response()
