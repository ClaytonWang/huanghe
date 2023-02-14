from fastapi import APIRouter, Depends
from source.services.monitor.node.serializers import NodeCreate, NodeDetailRes
from source.services.monitor.models.node import Node
from k8s.cluster_client import cc
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters

router_node = APIRouter()


@router_node.get(
    '/batch',
    description='查询节点列表',
    response_model=Page[NodeDetailRes],
    response_model_exclude_unset=True
)
async def list_node(query_params: QueryParameters = Depends(QueryParameters)):
    nodes = await Node.undeleted_nodes()
    p = await paginate(nodes.filter(
        **query_params.filter_
    ), params=query_params.params)
    for i, v in enumerate(p.data):
        p.data[i] = Node.gen_node_pagation_response(v)
    return p


@router_node.post(
    '',
    description='创建服务器节点'
)
async def create_node(ncr: NodeCreate):
    await cc.get_node_list(ncr)
