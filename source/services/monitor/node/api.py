# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/30 14:34
@Auth ： Z01
@File ：api.py
@Motto：You are the best!
"""

from fastapi import APIRouter
from utils.prometheus import pq
from basic.middleware.rsp import success_common_response
from k8s.cluster_client import cc

router_node = APIRouter()
@router_node.get(
    '/batch',
    description='查询节点列表'
)
def list_node():
    return cc.list_node()

@router_node.get(
    '/list',
    description='总列表'
)
def list_node():
    return cc.list_node()
