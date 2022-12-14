from fastapi import APIRouter, Depends, HTTPException, status, Path, Header, Request
from basic.middleware.rsp import success_common_response
from models import Volume
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from volume.serializers import VolumeCreateReq, VolumeEditReq, VolumeDetailRes
from basic.middleware.account_getter import AccountGetter, ProjectGetter, get_project

router_volume = APIRouter()


@router_volume.get(
    '/{volume_id}',
    description="存储盘详情",
    response_model=VolumeDetailRes
)
async def get_volume(volume_id: int = Path(..., ge=1, description="存储ID")
                     ):
    v = await Volume.get_by_id(volume_id)
    return VolumeDetailRes.parse_obj(v.gen_volume_pagation_response())


@router_volume.get(
    '',
    description="存储盘列表",
    response_model=Page[VolumeDetailRes],
)
async def list_volume(query_params: QueryParameters = Depends(QueryParameters)):
    volumes = await Volume.undeleted_volumes()
    p = await paginate(volumes.filter(
        **query_params.filter_
    ), params=query_params.params)
    for i, v in enumerate(p.data):
        p.data[i] = VolumeDetailRes.parse_obj(v.gen_volume_pagation_response())
    return p


@router_volume.post(
    '',
    description='创建存储盘',
)
async def create_volume(request: Request,
                        vcr: VolumeCreateReq):
    user: AccountGetter = request.user
    project: ProjectGetter = get_project(request.headers.get('authorization'), vcr.project.id)
    await Volume.objects.create(**Volume.gen_create_dict(user, project, vcr))
    return success_common_response()


@router_volume.put(
    '/{volume_id}',
    description='更新存储盘',
)
async def update_volume(request: Request,
                        ver: VolumeEditReq,
                        volume_id: int = Path(..., ge=1, description="存储ID")):
    # user: AccountGetter = request.user
    v = await Volume.get_by_id(volume_id)
    await v.update(**Volume.gen_edit_dict(ver))
    return success_common_response()


@router_volume.delete(
    '/{volume_id}',
    description='删除存储盘',
)
async def delete_volume(request: Request,
                        volume_id: int = Path(..., ge=1, description="存储ID")):
    # user: AccountGetter = request.user
    await Volume.set_deleted(volume_id)
    return success_common_response()


@router_volume.post(
    '/{volume_id}/reset',
    description='恢复已被删除的存储盘',
)
async def recover_volume(request: Request,
                         volume_id: int = Path(..., ge=1, description="存储ID")):
    # user: AccountGetter = request.user
    await Volume.cancel_deleted(volume_id)
    return success_common_response()
