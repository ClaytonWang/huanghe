from fastapi import APIRouter
from services.cluster.deployment.serializers import Deployment, DeploymentDeleteReq, DeploymentCreateReq, DeploymentListReq
from services.cluster.k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response

router_deployment = APIRouter()


@router_deployment.post(
    '',
    description='创建notebook',
)
def create_notebook(dcr: DeploymentCreateReq):
    cc.create_deployment(Deployment.parse_obj(dcr.gen_deployment_dict()))
    return success_common_response()


@router_deployment.post(
    '/batch',
    description='批量查询notebook',
)
def list_notebook(dlr: DeploymentListReq):
    return cc.list_deployment(dlr)


@router_deployment.delete(
    '',
    description='删除notebook',
)
def delete_notebook(ddr: DeploymentDeleteReq):
    cc.delete_deployment(ddr)
    return success_common_response()
