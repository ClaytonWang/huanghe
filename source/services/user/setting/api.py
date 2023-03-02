# -*- coding: utf-8 -*-
"""
    >File    : api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/29 19:11
"""
from fastapi import APIRouter, Depends, Request, HTTPException, status, Path
from models import User, Project, Permissions, OperationPms
from api.serializers import OwnerUserList
from setting.serializers import ProjectSetUser
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from project.service_request import query_notebook_by_project, query_job_by_project


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

    params_filter = query_params.filter_
    params_filter['project__in'] = project_ids
    result = await paginate(OperationPms.objects.select_related(
        ['user', 'project', 'permissions']
    ).filter(**params_filter), params=query_params.params)
    result = result.dict()
    data = result['data']
    for item in data:
        user_data = item.pop('user')
        user_data['user_id'] = user_data.pop('id')
        item.update(**user_data)
    return result


@router_setting.post(
    '/user',
    description='项目添加普通用户&设置权限',
    response_model={},
)
async def project_set_user(
        body: ProjectSetUser
):
    project = await Project.objects.select_related('member').get(id=body.project)
    user = await User.objects.get(id=body.user)
    add_pms = await Permissions.objects.filter(id__in=body.permissions).all()

    # TODO 失败回滚
    # 删除指定用户和项目的所有权限
    pms = await OperationPms.objects.get_or_none(project=project, user=user)
    pms and await pms.permissions.clear()

    if not pms:
        pms = await OperationPms.objects.create(**dict(
            project=project.id,
            user=user.id
        ))

    # 重新添加权限
    for _item in add_pms:
        await pms.permissions.add(_item)

    # 添加项目普通用户关联
    if user not in project.member:
        await project.member.add(user)


@router_setting.put(
    '/user/{pk}',
    description='项目编辑普通用户&设置权限',
    response_model={},
)
async def project_set_user(
        body: ProjectSetUser,
        pk: int = Path(..., ge=1, description='pms ID')
):
    project = await Project.objects.select_related('member').get(id=body.project)
    user = await User.objects.get(id=body.user)
    add_pms = await Permissions.objects.filter(id__in=body.permissions).all()

    # TODO 失败回滚
    # 删除指定用户和项目的所有权限
    pms = await OperationPms.objects.select_related(['user', 'project', 'project__member']).get_or_none(id=pk)
    await pms.permissions.clear()
    old_project = pms.project
    if user in old_project.member:
        await old_project.member.remove(user)
    await OperationPms.objects.filter(id=pk).update(project=project.id, user=user.id)

    # 重新添加权限
    for _item in add_pms:
        await pms.permissions.add(_item)

    # 添加项目普通用户关联
    if user not in project.member:
        await project.member.add(user)


@router_setting.delete(
    '/user/{pk}',
    description='删除【设置&用户项目权限】',
    response_model={},
)
async def project_set_user(
        request: Request,
        pk: int = Path(..., ge=1, description='权限模块ID')
):
    authorization: str = request.headers.get('authorization')
    pms = await OperationPms.objects.select_related(['user', 'project', 'project__member']).get(id=pk)
    # 从项目的普通成员中删除该用户
    _user = pms.user
    _project = pms.project
    notebook_list = query_notebook_by_project(authorization, _project.id, _user.id)
    if notebook_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联notebook，不能删除')
    if query_job_by_project(authorization, _project.id, _user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联job，不能删除')
    if _user in _project.member:
        await _project.member.remove(_user)
    await pms.permissions.clear()
    await pms.delete()
