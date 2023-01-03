# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/27 14:23
"""
import json
from typing import List, Dict
from fastapi import APIRouter, Depends, Request, HTTPException, status, Path
from fastapi.responses import JSONResponse
from models import Notebook, Status, Image, Source
from source.serializers import SourceList
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from collections import defaultdict


router_source = APIRouter()


@router_source.get(
    '',
    description='资源规格列表',
    response_model=Page[SourceList],
    response_model_exclude_unset=True
)
async def list_source(query_params: QueryParameters = Depends(QueryParameters),):
    params_filter = query_params.filter_
    result = await paginate(Source.objects.filter(**params_filter), params=query_params.params)
    result = result.dict()
    # print(result)
    data = result['data']
    for item in data:
        item['name'] = f"{item.pop('gpu')}*{item.pop('type')} {item.pop('cpu')}C {item.pop('memory')}G"
    return result
