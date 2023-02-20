# -*- coding: utf-8 -*-
"""
    >File    : api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/28 19:52
"""
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from models.project import Project
from project.serializers import ProjectCreate, ProjectList, ProjectEdit
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from basic.common.env_variable import get_string_variable
from pypinyin import lazy_pinyin, Style
from basic.middleware.account_getter import create_ns, Namespace, create_secret, SecretNamespace
from project.service_request import query_notebook_by_project, query_job_by_project
from typing import List

router_project = APIRouter()


@router_project.get(
    '/items',
    description='项目列表所有项目',
    response_model=List[ProjectList],
    response_model_exclude_unset=True
)
async def list_project_items():
    _projects = await Project.objects.select_related('owner').all()
    return _projects


@router_project.get(
    '/{project_id}',
    description="项目详情",
    response_model=ProjectList
)
async def get_project(project_id: int = Path(..., ge=1, description='需要查询的项目ID')):
    _project = await Project.objects.get(pk=project_id)
    return _project


@router_project.post(
    '',
    description='创建项目 关联用户类型暂时不做强制检查',
    response_model=ProjectList,
)
async def create_project(project: ProjectCreate):
    init_data = project.dict()
    en_name = ''.join(lazy_pinyin(init_data['name'] + init_data['code'], style=Style.FIRST_LETTER))
    init_data['en_name'] = f"{get_string_variable('ENV', 'DEV')}-{en_name}".lower()
    create_ns(Namespace(name=init_data['en_name']), ignore_exist=True)
    create_secret(SecretNamespace(namespace=init_data['en_name']), ignore_exist=True)
    return await Project.objects.create(**init_data)


@router_project.get(
    '',
    description='项目列表',
    response_model=Page[ProjectList],
    response_model_exclude_unset=True
)
async def list_project(
        query_params: QueryParameters = Depends(QueryParameters)
):
    """
    :param query_params:
    :return:
    """

    filter_params = query_params.filter_
    if filter_params and 'owner' in filter_params:
        owner = filter_params['owner']
        if not owner.isdigit():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f'参数{owner}类型错误'
            )
        filter_params['owner'] = int(owner)

    result = await paginate(
        Project.objects.select_related('owner').filter(**filter_params), params=query_params.params
    )
    return result


@router_project.put(
    '/{project_id}',
    description='更新项目信息',
    response_description='返回空',
)
async def update_project(
        project: ProjectEdit,
        project_id: int = Path(..., ge=1, description='需要更新的项目ID'),
):
    update_data = project.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新数据不能为空')
    _project = await Project.objects.get_or_none(pk=project_id)
    if not (_project and await _project.update(**update_data)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='项目不存在')
    return JSONResponse(dict(id=project_id))


@router_project.delete(
    '/{project_id}',
    description='删除项目（项目中没有成员且资源清空，可删除项目）',
    status_code=status.HTTP_200_OK,
)
async def delete_project(
        request: Request,
        project_id: int = Path(..., ge=1, description='项目ID')
):
    authorization: str = request.headers.get('authorization')
    project = await Project.objects.get(id=project_id)
    if await project.member.count():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联用户，不能删除')
    result = query_job_by_project(authorization, project_id=project_id)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联job，不能删除')

    notebook_list = query_notebook_by_project(authorization, project_id=project_id)
    if notebook_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联notebook，不能删除')

    await project.delete()
