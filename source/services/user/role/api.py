# -*- coding: utf-8 -*-
"""
    >File    : role_api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 09:04
"""
from typing import List
from fastapi import APIRouter, Depends
from models.user import Role
from role.serializers import RoleDetailSerializers
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

#
# @router_role.get(
#     '',
#     description='角色列表',
#     response_description='返回角色列表',
#     response_model=Page[RoleDetailSerializers]
# )
# async def list_role(params: Params = Depends()):
#     return await paginate(Role.objects.filter(), params=params)


@router_role.get(
    '',
    description='角色列表',
    response_description='返回角色列表',
    response_model=List[RoleDetailSerializers]
)
async def list_role():
    return await Role.objects.all()
