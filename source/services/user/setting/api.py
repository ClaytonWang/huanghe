# -*- coding: utf-8 -*-
"""
    >File    : api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/29 19:11
"""
from fastapi import APIRouter, Depends, Request, HTTPException, status
from models import User, Project, Permissions, OperationPms
from api.serializers import OwnerUserList
from setting.serializers import ProjectSetUser
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

    projects = await Project.objects.filter(owner=request.user).values_list(fields=['id'])
    project_ids = [item[0] for item in projects]

    result = await paginate(OperationPms.objects.select_related(['user', 'project', 'permissions']).filter(
        project__in=project_ids
    ), params=query_params.params)
    result = result.dict()
    data = result['data']
    for item in data:
        item.update(**item.get('user'))
    return result


@router_setting.post(
    '/user',
    description='项目添加普通用户&设置权限',
    response_model={},
)
async def project_set_user(
        body: ProjectSetUser
):
    project = await Project.objects.get(id=body.project)
    user = await User.objects.get(id=body.user)
    add_pms = await Permissions.objects.filter(id__in=body.access).all()

    # TODO 失败回滚
    # 删除指定用户和项目的所有权限
    pms = await OperationPms.objects.get_or_none(project=project, user=user)
    pms and pms.permissions.clear()

    if not pms:
        pms = await OperationPms.objects.create(**dict(
            project=project.id,
            user=user.id
        ))

    # 重新添加权限
    for _item in add_pms:
        await pms.permissions.add(_item)
