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
from pydantic import validator


class StatusItem(BaseModel):
    code: str = None
    name: str = None
    desc: str = None


class SourceItem(BaseModel):
    id: int
    cpu: int
    memory: int
    gpu: int


class UserStr(BaseModel):
    id: str
    username: str = None


class ProjectStr(BaseModel):
    id: str
    name: Optional[str] = None


class ImageItem(BaseModel):
    id: Optional[str]
    name: str
    desc: Optional[str] = None


class VolumeConfig(BaseModel):
    value: int
    size: int


class VolumeItem(BaseModel):
    name: str
    config: VolumeConfig


class HookItem(BaseModel):
    storage: VolumeItem
    path: str


class NotebookOp(BaseModel):
    action: int


class NotebookList(BaseModel):
    id: int
    status: StatusItem
    name: str
    source: str
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
    source: str = Field(..., max_length=80)
    project: ProjectStr
    image: ImageItem
    hooks: List[HookItem] = []


class NotebookCreateAfter(BaseModel):
    id: int
    status: StatusItem
    name: str
    creator_id: int
    project_id: int
    image_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class NotebookEdit(BaseModel):
    name: str = Field(..., max_length=20)
    source: Optional[str] = Field(..., max_length=80)
    project: ProjectStr
    image: Optional[ImageItem]
    projects: Optional[List[HookItem]] = []
