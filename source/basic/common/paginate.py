# -*- coding: utf-8 -*-
"""
    >File    : paging.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 15:08
"""
from __future__ import annotations
from abc import ABC
from fastapi import Query
from typing import Generic, Sequence, TypeVar
from typing import Union, Type, Optional
from contextvars import ContextVar
from pydantic import BaseModel, conint
from fastapi_pagination.bases import AbstractParams, RawParams
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.api import resolve_params
from ormar import Model, QuerySet

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    pageno: int = Query(1, ge=1, description="Page number")
    pagesize: int = Query(50, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.pagesize,
            offset=self.pagesize * (self.pageno - 1),
        )


class BasePage(AbstractPage[T], Generic[T], ABC):
    data: Sequence[T]
    total: conint(ge=0)  # type: ignore


class Page(BasePage[T], Generic[T]):
    pageno: conint(ge=1)  # type: ignore
    pagesize: conint(ge=1)  # type: ignore

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        data: Sequence[T],
        total: int,
        params: Params,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        return cls(
            total=total,
            data=data,
            pageno=params.pageno,
            pagesize=params.pagesize,
        )


page_type: ContextVar[Type[AbstractPage]] = ContextVar("page_type", default=Page)


def create_page(items: Sequence[T], total: int, params: AbstractParams) -> AbstractPage[T]:
    return page_type.get().create(items, total, params)


async def paginate(query: Union[QuerySet, Type[Model]], params: Optional[Params] = None) -> AbstractPage:
    if not isinstance(query, QuerySet):
        query = query.objects

    params = resolve_params(params)

    raw_params = params.to_raw_params()

    total = await query.count()
    items = await query.offset(raw_params.offset).limit(raw_params.limit).all()

    return create_page(items, total, params)


__all__ = ['Params', 'paginate', 'Page']
