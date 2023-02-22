from fastapi import APIRouter
from k8s.cluster_client import cc
from secret.serializers import SecretNamespace
from basic.middleware.rsp import success_common_response


router_secret = APIRouter()


@router_secret.post(
    '',
    description='创建默认华为云镜像密钥',
)
def create_secret(sn: SecretNamespace):
    cc.create_namespaced_secret(sn)
    return success_common_response()


# @router_secret.post(
#     '',
#     description='读取密钥',
# )
# def read_secret(sc: SecretCommon):
#     res = cc.read_namespaced_secret(sc)
#     print(res)
#     return success_common_response()
