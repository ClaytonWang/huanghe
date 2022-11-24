# -*- coding: utf-8 -*-
"""
    >File    : role_api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 09:04
"""
from fastapi import APIRouter, HTTPException, status, Depends
from models.user import Role
from api.role_serializers import RoleDetailSerializers
from fastapi.encoders import jsonable_encoder
from basic.common.paginate import Page
from basic.common.paginate import Params
from basic.common.paginate import paginate


router_role = APIRouter()


@router_role.post(
    "",
    response_model=RoleDetailSerializers,
    description='角色',
    response_description="创建角色信息"
)
async def add_role(role: Role):
    return await role.save()


@router_role.put(
    '',
    description='更新',
    responses={status.HTTP_204_NO_CONTENT: {'model': None}}
)
def update_role():
    pass


@router_role.delete(
    '',
    description='删除',
    responses={status.HTTP_204_NO_CONTENT: {'model': None}}
)
def delete_role():
    pass


@router_role.get(
    '',
    description='列表',
    response_model=Page[RoleDetailSerializers]
)
async def list_role(params: Params = Depends()):
    return await paginate(Role.objects.filter(), params=params)
