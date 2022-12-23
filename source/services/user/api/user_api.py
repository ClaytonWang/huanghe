# -*- coding: utf-8 -*-
"""
    >File    : views.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:10
"""
import ormar
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
    role = await Role.objects.get(name=user.role)
    if role.name == 'admin':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='不能创建管理员账号')

    # 用户英文名根据邮箱生成,创建后不能修改邮箱故不变,首字母为数字时添加前缀字符
    en_name = ''.join(filter(str.isalnum, user.email.split('@')[0]))
    en_name = 'u' + en_name if en_name[0].isdigit() else en_name
    init_data['en_name'] = en_name

    # TODO 失败回滚
    project_ids = init_data.pop('projects', [])
    # 把原始数据的role换成ID
    init_data['role'] = role.id
    new_user = await User.objects.create(**init_data)

    # 新建用户为普通用户时关联项目
    if project_ids and role.name == 'user':
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
    query_filter = query_params.filter_
    # 项目负责人不是项目成员之一，无法用projects__code获取
    if 'projects__code' in query_filter:
        projects_code = query_filter.pop('projects__code')
        code_filter = ormar.or_(projects__code=projects_code, project_user__code=projects_code)
        query_filter = ormar.and_(code_filter, **query_filter)
    if isinstance(query_filter, dict):
        query_filter = ormar.queryset.clause.FilterGroup(**query_filter)
    result = await paginate(User.objects.select_related(
        ['role', 'project_user', 'projects']
    ).filter(
        query_filter
    ), params=query_params.params)
    json_result = result.dict()
    data = json_result.get('data', [])
    for index, item in enumerate(data):
        if item.get('role') and item['role'].get('name') == 'admin':
            item['projects'] = []
        else:
            members_projects = item.get('projects', [])
            projects_list = item.get('project_user', []) + members_projects
            project_ids = set()
            res = []
            for project in projects_list:
                if project['id'] not in project_ids:
                    project_ids.add(project['id'])
                    res.append(project)
            item['projects'] = res
    return json_result


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
    role_name = None

    if 'role' in update_data:
        role = await Role.objects.get(name=update_data['role'])
        if role.name == 'admin':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='角色不能修改成管理员')
        update_data['role'] = role.id
        role_name = role.name

    project_ids = None
    if 'projects' in update_data:
        project_ids = update_data.pop('projects')

    _user = await User.objects.select_related(['role', 'projects']).get(pk=user_id)
    if update_data:
        _user = await _user.update(**update_data)
    if role_name is None:
        role_name = _user.role.name

    if project_ids is not None and role_name == 'user':
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
    user = await User.objects.get(id=user_id)
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
    # owner = request.user,
    projects = await Project.objects.select_related('member').filter(
        ormar.or_(owner=request.user, member__id=request.user.id)
    ).all()
    setattr(request.user, 'projects', projects)
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
            role_name: str = Query(default='owner', description='权限名，默认选择项目负责人'),
            project_id: str = Query(default='', description='权限名，默认选择项目负责人')
):
    """
    :param role_name:
    :return:
    """
    role_name = role_name.split(",")
    project_id = list(map(int, project_id.split(",")))
    if project_id:
        return await User.objects.select_related(['role', 'project_user', 'projects']).filter(projectuser__project__in=project_id).filter(role__name__in=role_name).all()


    return await User.objects.filter(role__name__in=role_name).all()
