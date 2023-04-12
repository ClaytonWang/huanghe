# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/27 14:25
"""
from fastapi import APIRouter, Depends, Request, HTTPException, status, Path
from models import Notebook, Status, Image, Source
from image.serializers import ImageItem
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters


router_image = APIRouter()


@router_image.get(
    '',
    description='镜像列表',
    response_model=Page[ImageItem],
    response_model_exclude_unset=True
)
async def list_images(query_params: QueryParameters = Depends(QueryParameters),):
    params_filter = query_params.filter_
    result = await paginate(Image.objects.filter(**params_filter), params=query_params.params)
    return result
