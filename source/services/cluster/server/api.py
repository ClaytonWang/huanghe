from fastapi import APIRouter
from k8s.cluster_client import cc

router_server = APIRouter()


@router_server.get(
    '',
    description='查询node信息',
)
def list_server():
    return cc.get_server_list()
