# -*- coding: utf-8 -*-
"""
    >File   : serializers.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/15 10:21
"""
import re
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from basic.utils.dt_format import dt_to_string
from image.serializers import ImageItem
from source.serializers import SourceList
from pydantic import validator


class StatusItem(BaseModel):
    code: str = None
    name: str = None
    desc: str = None


class UserStr(BaseModel):
    id: int
    username: str = None


class ProjectStr(BaseModel):
    id: int
    name: Optional[str] = None


class HookItem(BaseModel):
    storage: int
    path: str


class NotebookOp(BaseModel):
    action: int


class NotebookList(BaseModel):
    id: int
    status: StatusItem
    name: str
    source: Optional[SourceList]
    creator: Optional[UserStr]
    project: Optional[ProjectStr]
    image: ImageItem
    url: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        return dt_to_string(dt, '%Y-%m-%d')


class NotebookCreate(BaseModel):
    name: str = Field(..., max_length=20)
    source: str
    project: str
    image: str
    hooks: List[HookItem] = []

    @validator('name')
    def notebook_name_validator(cls, name):
        if not name or not re.match('^[a-zA-Z][0-9a-zA-Z]*$', name):
            raise ValueError("Notebook命名必须为英文数字组合且首位必须是字母")
        return name.lower()


class NotebookDetail(BaseModel):
    id: int
    status: StatusItem
    name: str
    source: int
    creator: int
    project: int
    image: int
    hooks: List[HookItem]
    url: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class NotebookEdit(BaseModel):
    name: str = Field(..., max_length=20)
    source: Optional[str]
    project: Optional[str]
    image: Optional[str]
    hooks: Optional[List[HookItem]] = []

    @validator('name')
    def notebook_name_validator(cls, name):
        if not name or not re.match('^[a-zA-Z][0-9a-zA-Z]*$', name):
            raise ValueError("Notebook命名必须为英文数字组合且首位必须是字母")
        return name.lower()
