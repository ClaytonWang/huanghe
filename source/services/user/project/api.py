# -*- coding: utf-8 -*-
"""
    >File    : api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/28 19:52
"""
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from models.project import Project
from project.serializers import ProjectCreate, ProjectList, ProjectEdit
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters


router_project = APIRouter()


@router_project.post(
    '',
    description='创建项目',
    response_model=ProjectList,
)
async def create_project(project: ProjectCreate):
    return await Project.objects.create(**project.dict())


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
    return await paginate(Project.objects.select_related('owner'), params=query_params.params)


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
        project_id: int = Path(..., ge=1, description='项目ID')
):

    project = await Project.objects.get_or_none(id=project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='未查询到项目')

    count = await project.member.count()
    if count:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联用户，不能删除')

    await project.delete()
