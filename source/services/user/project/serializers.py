# -*- coding: utf-8 -*-
"""
    >File    : serializer.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/28 19:45
"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from basic.utils.dt_format import dt_to_string
from pydantic import validator
from api.serializers import UserId


class ProjectCreate(BaseModel):
    code: str = Field(..., max_length=80)
    name: str = Field(..., max_length=80)
    owner: int = Field(...)


class ProjectList(BaseModel):
    code: str
    name: str
    owner: UserId
    project: Optional[List[int]] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        return dt_to_string(dt)
