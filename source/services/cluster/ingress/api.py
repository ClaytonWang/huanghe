from fastapi import APIRouter
from services.cluster.ingress.serializers import Ingress
from services.cluster.k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response

router_ingress = APIRouter()


@router_ingress.post(
    '',
    description='创建华为云容器路由',
)
def create_network(ig: Ingress):
    cc.create_ingress(ig=ig)
    return success_common_response()


# @router_namespace.delete(
#     '',
#     description='删除命名空间',
#     response_model=Namespace,
# )
# def delete_namespace(ns: Namespace):
#     cc.delete_namespace(ns)
#     return success_common_response()
