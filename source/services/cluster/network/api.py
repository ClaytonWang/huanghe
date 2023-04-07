from fastapi import APIRouter
from services.cluster.network.serializers import Network
from services.cluster.k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response

router_network = APIRouter()


@router_network.post(
    '',
    description='创建华为云容器网络',
)
def create_network(nw: Network):
    cc.create_network(nw)
    return success_common_response()


# @router_namespace.delete(
#     '',
#     description='删除命名空间',
#     response_model=Namespace,
# )
# def delete_namespace(ns: Namespace):
#     cc.delete_namespace(ns)
#     return success_common_response()
