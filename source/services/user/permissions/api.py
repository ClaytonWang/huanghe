# -*- coding: utf-8 -*-
"""
    >File    : permissions_api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 09:04
"""
from fastapi import APIRouter, Query, HTTPException, status
from models import Permissions
from permissions.services import role_pms, join_pms_item


router_pms = APIRouter()


@router_pms.get(
    '/role',
    description='根据角色返回权限因子',
)
async def list_role(role: str):
    return await role_pms(role)


@router_pms.get(
    '/menu',
    description='根据菜单获取权限',
)
async def list_role(
        name: str = Query(..., description='权限名称')
):
    pms = await Permissions.objects.get_or_none(name=name)
    if not pms:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='没有菜单')

    pms = await Permissions.objects.filter(code__icontains=pms.code).order_by('code').fields(
        ['code', 'name', 'value']).values()
    order_pms = sorted(pms, key=lambda item: int(item['code']))
    results = []
    for _item in order_pms:
        results = join_pms_item(_item, results, level=0)
    return results

