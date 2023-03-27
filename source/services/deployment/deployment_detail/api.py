# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 17:29
@Auth ： Z01
@File ：api.py
@Motto：You are the best!
"""

from typing import List
from fastapi import APIRouter, Request, Path
from services.deployment.utils.hw_request import get_chart_hw
from services.deployment.deployment_detail.serializers import  TimeReq, SingleChart


router_deployment_detail = APIRouter()





@router_deployment_detail.post(
    '/:{deployment_id}/monitor',
    description='服务部署监控',
    response_model=List[SingleChart],
    response_model_exclude_unset=True
)
async def deployment_monitor(deployment_id: int = Path(..., ge=1, description="DeploymentID"),TimeReq:TimeReq=None):
    return get_chart_hw(TimeReq.start, TimeReq.end)
    # return get_chart_hw("2023-03-21 08:05:00", "2023-03-21 09:17:00")


@router_deployment_detail.post(
    '/:{deployment_id}/log',
    description='服务部署日志',
    # response_model=List[TaskItem],
    response_model_exclude_unset=True
)
async def deployment_monitor(deployment_id: int = Path(..., ge=1, description="DeploymentID"),TimeReq:TimeReq=None):
    return get_chart_hw(TimeReq.start, TimeReq.end)




