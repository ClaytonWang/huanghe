# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 17:29
@Auth ： Z01
@File ：api.py
@Motto：You are the best!
"""

from fastapi import APIRouter, Request
from overview.serializers import ProjectReq

router_overview = APIRouter()


@router_overview.post(
    '/tasks',
    description='开发统计',
    response_model_exclude_unset=True
)
async def task_statistic(request: Request, projects: ProjectReq):
    return [{
        "name": "Notebook",
        "total": 10,
        "running": 2
    }, {
        "name": "Job",
        "total": 12,
        "running": 1
    }]


@router_overview.post(
    '/sources',
    description='资源统计',
    response_model_exclude_unset=True
)
async def sources_statistic(request: Request, projects: ProjectReq):
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
