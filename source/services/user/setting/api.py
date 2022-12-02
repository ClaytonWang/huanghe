# -*- coding: utf-8 -*-
"""
    >File    : api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/29 19:11
"""
import copy
from fastapi import APIRouter, Depends, Request, HTTPException, status
from models import User, Role, Project
from api.serializers import OwnerUserList
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters


router_setting = APIRouter()


@router_setting.get(
    '/user',
    description='设置模块，用户列表（项目负责人才可以查看）',
    response_model=Page[OwnerUserList],
    response_model_exclude_unset=True
)
async def list_user(
        request: Request,
        query_params: QueryParameters = Depends(QueryParameters)
):
    """
    :param request:
    :param query_params:
    :return:
    """
    if request.user.role.name != 'owner':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='用户没有权限')

    filter_params = query_params.filter_
    filter_params['role__name'] = 'owner'
    # 未关联项目查询条件
    # filter_params['projects__id__isnull'] = False
    result = await paginate(User.objects.select_related('projects').filter(
        **query_params.filter_
    ), params=query_params.params)

    result = result.dict()
    data = result.get('data', [])
    new_data = []
    for item in data:
        projects = item.pop('projects')
        if not projects:
            item['project'] = {}
            new_data.append(item)
            continue

        for pro in projects:
            new_item = copy.deepcopy(item)
            new_item['project'] = pro
            new_data.append(new_item)
    result['data'] = new_data
    return result
