# -*- coding: utf-8 -*-
"""
    >File    : exception.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/27 10:36
"""
from fastapi import status
from fastapi.responses import JSONResponse
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError, DataError


def validation_pydantic_exception_handler(request, exc):
    """
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


def validation_ormar_exception_handler(request, exc):
    """
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


def ormar_db_exception_handler(request, exc):
    """
    :param request:
    :param exc:
    :return:
    """
    if isinstance(exc, (UniqueViolationError, ForeignKeyViolationError, DataError)):
        return JSONResponse(
            exc.detail if hasattr(exc, 'detail')
            and getattr(exc, 'detail') is not None
            and len(str(exc.detail)) else str(exc),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return exc
