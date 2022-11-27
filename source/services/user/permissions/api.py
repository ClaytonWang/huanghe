# -*- coding: utf-8 -*-
"""
    >File    : permissions_api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 09:04
"""
from fastapi import APIRouter
from permissions.services import role_pms


router_pms = APIRouter()


@router_pms.get(
    '/role',
    description='根据角色返回权限因子',
)
async def list_role(role: str):
    return await role_pms(role)
