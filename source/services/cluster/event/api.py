from fastapi import APIRouter
from services.cluster.event.serializers import Event
from services.cluster.k8s.cluster_client import cc
router_event = APIRouter()


@router_event.post(
    '/batch',
    description='批量查询事件',
)
def list_event(event: Event):
    return cc.list_event(event)
