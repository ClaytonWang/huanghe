# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 17:29
@Auth ： Z01
@File ：api.py
@Motto：You are the best!
"""

from typing import List
from fastapi import APIRouter, Request
from services.monitor.overview.serializers import TaskItem
from basic.middleware.service_requests import get_user_list, get_notebook_list, get_job_list


router_overview = APIRouter()


async def generate_filter_path(request, authorization, project_ids):
    role_name = request.user.role.name
    user_list = await get_user_list(authorization)
    id_proj_map = {x['id']: x['project_ids'] for x in user_list}

    filter_list = []
    viewable_project_ids = set()

    if role_name != 'admin':
        viewable_project_ids = id_proj_map.get(request.user.id)
    if role_name == 'user':
        filter_list.append(f'filter[creator_id]={request.user.id}')

    if isinstance(project_ids, str):
        project_ids = [int(x) for x in project_ids.split(',')]
    if viewable_project_ids:
        viewable_project_ids = set(viewable_project_ids).intersection(set(project_ids))
    else:
        viewable_project_ids = project_ids

    if viewable_project_ids:
        project_str = ','.join([str(x) for x in viewable_project_ids])
        filter_list.append(f'filter[project_ids]={project_str}')
    # print(filter_list)
    filter_path = '?' + '&'.join(filter_list) if filter_list else None
    # print(filter_path)
    return filter_path


@router_overview.get(
    '/tasks',
    description='开发统计',
    response_model=List[TaskItem],
    response_model_exclude_unset=True
)
async def task_statistic(request: Request,
                         project: str = None):
    authorization: str = request.headers.get('authorization')

    if not project:
        return [{"name": "Notebook", "total": 0, "running": 0},
                {"name": "Job", "total": 0, "running": 0}]

    result = await generate_filter_path(request, authorization, project)

    notebook = await get_notebook_list(authorization, result)
    total_running = list(filter(lambda x: x['status'] == 'running', notebook))
    res_note = {
        "name": "Notebook",
        "total": len(notebook),
        "running": len(total_running)
    }

    job = await get_job_list(authorization, result)
    total_job_running = list(filter(lambda x: x['status'] == 'run', job))
    res_job = {
        "name": "Job",
        "total": len(job),
        "running": len(total_job_running)
    }

    return [res_note, res_job]


# @router_overview.get(
#     '/sources',
#     description='资源统计',
#     response_model_exclude_unset=True
# )
# async def sources_statistic(request: Request, project: str = None):
#     authorization: str = request.headers.get('authorization')
#
#     if not project:
#         return [
#             {
#                 "name": "CPU",
#                 "occupied": 0,
#                 "used": 0,
#                 "occupied_rate": 0,
#             },
#             {
#                 "name": "GPU",
#                 "occupied": 0,
#                 "used": 0,
#                 "occupied_rate": 0,
#             },
#             {
#                 "name": "内存",
#                 "occupied": 0,
#                 "used": 0,
#                 "occupied_rate": 0,
#             },
#             {
#                 "name": "存储",
#                 "occupied": 0,
#                 "used": 0,
#                 "occupied_rate": 0,
#             },
#         ]
#
#     result = await generate_filter_path(request, authorization, project)
#
#     notebook = await get_notebook_list(authorization, result)
#     occupied_cpu = sum([x['cpu'] for x in notebook])
#     occupied_gpu = sum([x['gpu'] for x in notebook])
#     occupied_mem = sum([x['memory'] for x in notebook])
#     occupied_size = sum([x['storage_size'] for x in notebook])
#
#     pod_tuple = [(x['namespace_name'], x['pod_name'], x['cpu']) for x in notebook]
#
#     for x in notebook:
#         print(x['name'], x['status'])
#         get_prometheus_query(x['namespace_name'], x['pod_name'], x['cpu'])
#
#     return [
#         {
#             "name": "CPU",
#             "occupied": occupied_cpu,
#             "used": 10,
#             "occupied_rate": 0.5,
#         },
#         {
#             "name": "GPU",
#             "occupied": occupied_gpu,
#             "used": 10,
#             "occupied_rate": 0.5,
#         },
#         {
#             "name": "内存",
#             "occupied": occupied_mem,
#             "used": 10,
#             "occupied_rate": 0.5
#         },
#         {
#             "name": "存储",
#             "occupied": occupied_size,
#             "used": 10,
#             "occupied_rate": 0.5
#         },
#     ]
