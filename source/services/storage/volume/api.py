from fastapi import APIRouter, Depends, HTTPException, status, Path, Header, Request
from basic.middleware.rsp import success_common_response
from models import Volume
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from volume.serializers import VolumeCreateReq, VolumeEditReq, VolumeDetailRes
from basic.middleware.account_getter import AccountGetter, ProjectGetter, get_project,\
    ADMIN, USER, create_pvc, delete_pvc,PVCCreateReq, PVCDeleteReq, query_notebook_volume

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
async def list_volume(request: Request,
                      query_params: QueryParameters = Depends(QueryParameters)):
    user: AccountGetter = request.user
    volumes = await Volume.undeleted_volumes() if user.role.name == ADMIN else await Volume.undeleted_self_project_volumes([project.id for project in user.projects])
    if query_params.filter_.get("isdeleted", False):
        query_params.filter_.pop("isdeleted")
        query_params.filter_["deleted_at"] = None
        query_params.filter_["owner_by_id"] = user.id
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
    if user.role.name != ADMIN and vcr.config.size > 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{user.role.name}只能创建1024以内大小的存储')
    if await Volume.objects.filter(name=vcr.name, project_by_id=project.id, created_by_id=user.id).exists():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'同一个项目下，同一个用户，不能创建相同名称的盘')
    create_pvc(PVCCreateReq(name=f"{user.en_name}-{vcr.name}", namespace=project.en_name, size=vcr.config.size),
               ignore_exist=True)
    await Volume.objects.create(**Volume.gen_create_dict(user, project, vcr))
    return success_common_response()


@router_volume.put(
    '/{volume_id}',
    description='更新存储盘',
)
async def update_volume(request: Request,
                        ver: VolumeEditReq,
                        volume_id: int = Path(..., ge=1, description="存储ID")):
    user: AccountGetter = request.user
    v = await Volume.get_by_id(volume_id)
    d = {}
    if ver.project.id and v.project_by_id != ver.project.id:
        project: ProjectGetter = get_project(request.headers.get('authorization'), ver.project.id)
        if await Volume.objects.filter(name=v.name, project_by_id=project.id, created_by_id=user.id).exists():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'同一个项目下，同一个用户，不能创建相同名称的盘')
        size = ver.config.size if ver.config.size and ver.config.size > v.size else v.size
        # create new project pvc
        create_pvc(PVCCreateReq(name=f"{v.create_en_by}-{v.name}", namespace=project.en_name, size=size),
                   ignore_exist=True)
        d.update({"project_by_id": project.id,
                  "project_by": project.name,
                  "project_en_by": project.en_name,})
    if ver.config.size and ver.config.size < v.size:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'输入的更新值不能小于当前值')
    if ver.config.size and ver.config.size > v.size:
        if user.role == ADMIN and v.max == 1024:
            d.update({"max": 9999999})
        d.update({"size": ver.config.size})
    if ver.owner and ver.owner.id != v.owner_by_id:
        d.update({"owner_by": ver.owner.username,
                  "owner_by_id": ver.owner.id})
    await v.update(**d)
    return success_common_response()


@router_volume.delete(
    '/{volume_id}',
    description='删除存储盘',
)
async def delete_volume(request: Request,
                        volume_id: int = Path(..., ge=1, description="存储ID")):
    user: AccountGetter = request.user
    result = query_notebook_volume(request.headers.get('authorization'), volume_id)
    if len(result) != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'还存留notebook挂载这个盘， 不能删除')
    await Volume.set_deleted(volume_id, user.id)
    return success_common_response()


@router_volume.post(
    '/{volume_id}/reset',
    description='恢复已被删除的存储盘',
)
async def recover_volume(request: Request,
                         volume_id: int = Path(..., ge=1, description="存储ID")):
    user: AccountGetter = request.user
    await Volume.cancel_deleted(volume_id, user.id)
    return success_common_response()
