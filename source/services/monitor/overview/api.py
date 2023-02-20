# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 17:29
@Auth ： Z01
@File ：api.py
@Motto：You are the best!
"""

from typing import List, Dict
from fastapi import APIRouter, Request, Depends
from basic.common.query_filter_params import QueryParameters
from overview.serializers import ProjectReq, TaskItem
from utils.service_requests import get_user_list, get_notebook_list, get_job_list


router_overview = APIRouter()


@router_overview.get(
    '/tasks',
    description='开发统计',
    response_model=List[TaskItem],
    response_model_exclude_unset=True
)
async def task_statistic(request: Request,
                         project: str = None):
    authorization: str = request.headers.get('authorization')
    role_name = request.user.role.name

    user_list = await get_user_list(authorization)
    id_proj_map = {x['id']: x['project_ids'] for x in user_list}
    viewable_project_ids = set()

    filter_list = []

    if role_name != 'admin':
        viewable_project_ids = id_proj_map.get(request.user.id)
    if role_name == 'user':
        filter_list.append(f'filter[created_by_id]={request.user.id}')

    if project:
        project_ids = project
        if isinstance(project_ids, str):
            project_ids = [int(x) for x in project_ids.split(',')]
        if viewable_project_ids:
            viewable_project_ids = set(viewable_project_ids).intersection(set(project_ids))
        else:
            viewable_project_ids = project_ids
    else:
        return [{"name": "Notebook", "total": 0, "running": 0},
                {"name": "Job", "total": 0, "running": 0}]

    # print(viewable_project_ids)
    if viewable_project_ids:
        project_str = ','.join([str(x) for x in viewable_project_ids])
        filter_list.append(f'filter[project_ids]={project_str}')
    # print(filter_list)
    filter_path = '?' + '&'.join(filter_list) if filter_list else None
    # print(filter_path)

    notebook = await get_notebook_list(authorization, filter_path)
    total_running = list(filter(lambda x: x['status'] == 'running', notebook))
    res_note = {
        "name": "Notebook",
        "total": len(notebook),
        "running": len(total_running)
    }

    job = await get_job_list(authorization, filter_path)
    total_job_running = list(filter(lambda x: x['status'] == 'run', job))
    res_job = {
        "name": "Job",
        "total": len(job),
        "running": len(total_job_running)
    }

    return [res_note, res_job]


@router_overview.get(
    '/sources',
    description='资源统计',
    response_model_exclude_unset=True
)
async def sources_statistic(request: Request):
    return [
        {
            "name": "CPU",
            "occupied": 24,
            "used": 10,
            "occupied_rate": 0.5,
        },
        {
            "name": "GPU",
            "occupied": 24,
            "used": 10,
            "occupied_rate": 0.5,
        },
        {
            "name": "内存",
            "occupied": 24,
            "used": 10,
            "occupied_rate": 0.5
        },
        {
            "name": "存储",
            "occupied": 24,
            "used": 10,
            "occupied_rate": 0.5
        },
    ]
