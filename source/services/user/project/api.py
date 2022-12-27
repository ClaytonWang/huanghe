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
from pypinyin import lazy_pinyin, Style
from basic.middleware.account_getter import create_ns, delete_ns, Namespace

router_project = APIRouter()


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
    # TODO 避免首字母冲突
    en_name = ''.join(lazy_pinyin(init_data['name'], style=Style.FIRST_LETTER)).upper()
    init_data['en_name'] = 'U' + en_name if en_name[0].isdigit() else en_name
    create_ns(Namespace(name=init_data['en_name']))
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
    if 'name' in update_data:
        en_name = ''.join(lazy_pinyin(update_data['name'], style=Style.FIRST_LETTER)).upper()
        update_data['en_name'] = 'U' + en_name if en_name[0].isdigit() else en_name
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

    project = await Project.objects.get(id=project_id)
    if await project.member.count():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='存在关联用户，不能删除')
    delete_ns(Namespace(name=project.en_name))

    await project.delete()
