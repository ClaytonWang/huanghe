# -*- coding: utf-8 -*-
"""
    >File    : permissions_serializers.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 09:04
"""
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class PmsRspMode(str, Enum):
    string = 'string',
    tree = 'tree'


class PmsListQueryParams(BaseModel):
    mode: PmsRspMode = PmsRspMode.string
    role: Optional[str]
    code: Optional[str]


class PmsSerializers(BaseModel):
    id: int = None
    name: str = ''
    value: Optional[str]
    code: str
