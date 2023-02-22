from fastapi import APIRouter, Depends
from servers.serializers import ServerCreateReq, NodeDetailRes
from models.server import Server
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters

router_servers = APIRouter()


@router_servers.get(
    '',
    description='查询节点列表',
    # response_model=Page[NodeDetailRes],
    response_model_exclude_unset=True
)
async def list_server(query_params: QueryParameters = Depends(QueryParameters)):
    nodes = await Server.all_servers()
    p = await paginate(nodes.filter(
        # **query_params.filter_
    ), params=query_params.params)
    for i, v in enumerate(p.data):
        p.data[i] = Server.gen_server_pagation_response(v)
    return p