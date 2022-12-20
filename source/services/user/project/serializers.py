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
from api.serializers import UserItem


class ProjectCreate(BaseModel):
    code: str = Field(..., max_length=80)
    name: str = Field(..., max_length=80)
    owner: int = Field(...)


class ProjectList(BaseModel):
    id: int
    code: str
    name: str
    en_name: str
    owner: UserItem
    project: Optional[List[int]] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        return dt_to_string(dt, '%Y-%m-%d')


class ProjectEdit(BaseModel):
    code: str = Field(None, max_length=80)
    name: str = Field(None, min_length=1, max_length=255)
    owner:  Optional[int] = None
