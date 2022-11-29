# -*- coding: utf-8 -*-
"""
    >File    : views.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:10
"""
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from models import User, Role, Project
from api.serializers import AdminUserList
from api.serializers import UserList, UserCreate, UserEdit, AccountInfo
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from permissions.services import role_pms


router_user = APIRouter()


@router_user.post(
    '',
    description='创建用户',
    response_model=UserList,
)
async def create_user(user: UserCreate):

    init_data = user.dict()
    role = await Role.objects.get_or_none(id=user.role)
    if role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='角色无效')
    if role.name == 'admin':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='不能创建管理员账号')

    project_ids = init_data.pop('project', [])
    new_user = await User.objects.create(**init_data)

    if role.name == 'owner':
        projects = await Project.objects.filter(id__in=project_ids).all()
        for _project in projects:
            await _project.member.add(new_user)
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
    description='更新用户信息',
    response_description='返回空',
)
async def update_user(
        user: UserEdit,
        user_id: int = Path(..., ge=1, description='需要更新的用户ID'),
):
    update_data = user.dict(exclude_unset=True)
    _user = await User.objects.get_or_none(pk=user_id)
    if not (_user and await _user.update(**update_data)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='用户不存在')
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
    pass


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
