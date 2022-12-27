# -*- coding: utf-8 -*-
"""
    >File   : serializers.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/15 10:21
"""
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
    id: str
    username: str = None


class ProjectStr(BaseModel):
    id: str
    name: Optional[str] = None


class VolumeConfig(BaseModel):
    value: int
    size: int


class VolumeItem(BaseModel):
    name: str
    config: VolumeConfig


class HookItem(BaseModel):
    storage: int
    path: str


class StorageItem(BaseModel):
    storage: VolumeItem
    path: str


class NotebookOp(BaseModel):
    action: int


class NotebookList(BaseModel):
    id: str
    status: StatusItem
    name: str
    source: Optional[SourceList]
    creator: Optional[UserStr]
    project: Optional[ProjectStr]
    image: ImageItem
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
        # todo 要符合k8s的命名，全英文
        return name


class NotebookDetail(BaseModel):
    id: int
    status: StatusItem
    name: str
    source: SourceList
    creator_id: int
    project_id: int
    image_id: int
    hooks: List[StorageItem]
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
        # todo 要符合k8s的命名，全英文
        return name
