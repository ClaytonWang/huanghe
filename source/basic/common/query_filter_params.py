# -*- coding: utf-8 -*-
"""
    >File    : query_filter_params.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/27 14:16
"""
from typing import Optional
from fastapi import Query, Depends
from basic.common.paginate import Params


def query_parameters(
        params: Params = Depends(Params),
        sort: Optional[str] = Query(None, regex='[A-Za-z_]+:[desc|asc]+', example='id:desc'),
):
    return {
        params: params,
        sort: sort,
    }


class QueryParameters:
    def __init__(
            self,
            params: Params = Depends(Params),
            sort: Optional[str] = Query(None, regex='[A-Za-z_]+:[desc|asc]+', example='id:desc'),
                 ):
        self.params: Params = params
        self.sort: str = sort
