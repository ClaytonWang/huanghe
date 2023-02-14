# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 17:29
@Auth ： Z01
@File ：api.py
@Motto：You are the best!
"""

from fastapi import APIRouter, Request
from services.monitor.statistics.serializers import StatisticNoteBookReq, ProjectReq

router_statistic = APIRouter()


@router_statistic.get(
    '/task',
    description='开发统计',
    response_model_exclude_unset=True
)
async def notebook_job_statistic(request: Request, projects: ProjectReq, snb: StatisticNoteBookReq):
    return [{
        "name": "Notebook",
        "total": 10,
        "running": 2
    }, {
        "name": "Job",
        "total": 12,
        "running": 1
    }]


@router_statistic.get(
    '/sources',
    description='资源统计',
    response_model_exclude_unset=True
)
async def notebook_job_statistic(request: Request, projects: ProjectReq, snb: StatisticNoteBookReq):
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
