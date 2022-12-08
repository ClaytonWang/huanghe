from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from models import Volume
from volume.serializers import VolumeList
# from k8s.cluster_client import cc


router_volume = APIRouter()


@router_volume.post(
    '',
    description='创建存储盘',
    response_model=VolumeList,
)
async def create_volume(volume: Volume):
    return await Volume.objects.create(**volume.dict())





# @router_volume.delete(
#     '',
#     description='删除',
#     response_model=Namespace,
# )
# def delete_volume(volume: Volume):
#     cc.delete_namespace(volume)
#     return ns