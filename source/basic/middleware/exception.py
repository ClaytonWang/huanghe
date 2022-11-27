# -*- coding: utf-8 -*-
"""
    >File    : exception.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/27 10:36
"""
from fastapi import status
from fastapi.responses import JSONResponse


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
