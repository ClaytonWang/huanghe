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
from project.service_request import get_volume_list


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
        request: Request,
        user_id: int = Path(..., ge=1, description='用户ID')
):
    authorization: str = request.headers.get('authorization')
    user = await User.objects.get(id=user_id)
    owner_proj = await Project.objects.filter(owner=user).all()
    if await user.projects.count() or owner_proj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联项目资源不能删除')
    # 判断用户管理资源, 存储与项目解绑后需要清空关联存储
    volume_list = await get_volume_list(authorization)
    volume_filter = list(filter(lambda x: x['owner_id'] == user_id and x['deleted_at'] is None, volume_list))
    if volume_filter:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联存储不能删除')

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
    response_model=List[AdminUserList],
    response_model_exclude_unset=True
)
async def list_user(
            role_name: str = Query(None, description='权限名'),
            project_id: str = Query(None, description='项目名')
):
    """
    :param role_name:
    :param project_id:
    :return:
    """
    params_filter = dict()
    if role_name:
        role_names = role_name.split(",")
        params_filter['role__name__in'] = role_names
    if project_id:
        project_ids = list(map(int, project_id.split(",")))
        code_filter = ormar.or_(projectuser__project__in=project_ids, project_user__id__in=project_ids)
        params_filter = ormar.and_(code_filter, **params_filter)
    if isinstance(params_filter, dict):
        params_filter = ormar.queryset.clause.FilterGroup(**params_filter)
    result = await User.objects.select_related(['role', 'project_user', 'projects']).filter(params_filter).all()
    data = []
    for item in result:
        item = item.dict()
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
        data.append(item)
    return data
