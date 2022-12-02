# -*- coding: utf-8 -*-
"""
    >File    : views.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:10
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from models import User, Role, Project
from api.serializers import AdminUserList
from api.serializers import UserList, UserCreate, UserEdit
from api.serializers import AccountInfo, AccountEdit, UserItem
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from permissions.services import role_pms
from api.services import update_user_of_project
from auth.services import verify_password


router_user = APIRouter()


@router_user.post(
    '',
    description='创建用户',
    response_model=UserList,
)
async def create_user(user: UserCreate):

    init_data = user.dict()
    role = await Role.objects.get_or_none(id=user.role)
    if not role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='角色无效')
    if role.name == 'admin':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='不能创建管理员账号')

    # TODO 失败回滚
    project_ids = init_data.pop('project', [])
    new_user = await User.objects.create(**init_data)

    if role.name == 'owner':
        await update_user_of_project(project_ids=project_ids, user=new_user)
    return new_user


@router_user.get(
    '',
    description='用户列表（管理员）',
    response_model=Page[AdminUserList],
    response_model_exclude_unset=True
)
async def list_user(
        query_params: QueryParameters = Depends(QueryParameters)
):
    """
    :param query_params:
    :return:
    """
    return await paginate(User.objects.select_related(['role', 'projects']).filter(
        **query_params.filter_
    ), params=query_params.params)


@router_user.put(
    '/{user_id}',
    description='更新用户信息，角色不能更新成管理员',
    response_description='返回空',
)
async def update_user(
        user: UserEdit,
        user_id: int = Path(..., ge=1, description='需要更新的用户ID'),
):
    update_data = user.dict(exclude_unset=True)

    if 'role' in update_data:
        role = await Role.objects.get_or_none(id=update_data['role'])
        if not role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='角色无效')
        if role.name == 'admin':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='角色不能修改成管理员')

    project_ids = []
    if 'project' in update_data:
        project_ids = update_data.pop('project')

    _user = await User.objects.get_or_none(pk=user_id)
    if not _user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='用户不存在')

    if update_data:
        _user = await _user.update(**update_data)

    if project_ids:
        await update_user_of_project(project_ids=project_ids, user=_user, delete_old=True)

    return JSONResponse(dict(id=user_id))


@router_user.delete(
    '/{user_id}',
    description='删除用户',
    status_code=status.HTTP_200_OK,
)
async def delete_user(
        user_id: int = Path(..., ge=1, description='用户ID')
):
    user = await User.objects.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到用户')

    # TODO 判断用户管理资源
    if await user.projects.count():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联项目资源不能删除')

    await user.delete()


@router_user.get(
    '/account',
    response_description='请求用户名（姓名）、邮箱、角色、所属项目、权限、创建时间信息'
)
async def account(request: Request):
    if not hasattr(request, 'user') or not hasattr(request.user, 'role'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='未登录或角色不存在')

    result = AccountInfo.from_orm(request.user).dict()
    pms_info = await role_pms(request.user.role.name)
    result['permissions'] = pms_info
    # result['permissions'] = role_pms(request.user.role.name)
    return JSONResponse(result)


@router_user.post(
    '/account',
    response_description='更新个人账号信息，姓名和修改密码'
)
async def account(
        request: Request,
        user_info: AccountEdit,
):
    update_data = dict()
    # 修改用户名
    if user_info.username != request.user.username:
        update_data['username'] = user_info.username

    # 修改密码
    # 旧密码有一个输入，做密码更新校验
    if user_info.old_password or user_info.password:
        if not verify_password(user_info.old_password, request.user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='原始密码错误'
            )
        if user_info.password is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='需要输入新密码'
            )
        update_data['password'] = user_info.password

    len(update_data) and await request.user.update(**update_data)
    return JSONResponse({})


@router_user.get(
    '/items',
    description='用户列表指定类型的所有用户，字段只返回ID、用户名和邮箱',
    response_model=List[UserItem],
    response_model_exclude_unset=True
)
async def list_user(
            role_name: str = Query(default='owner', description='权限名，默认选择项目负责人')
):
    """
    :param role_name:
    :return:
    """
    return await User.objects.filter(role__name=role_name).all()
