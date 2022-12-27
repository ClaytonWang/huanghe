# -*- coding: utf-8 -*-
"""
    >File   : serializers.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/27 14:23
"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from basic.utils.dt_format import dt_to_string
from pydantic import validator


class SourceItem(BaseModel):
    id: int
    cpu: int
    memory: int
    gpu: int


class SourceList(BaseModel):
    id: str
    source: str
