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


def k8s_format(name):
    if not name or not re.match('^[a-zA-Z][0-9a-zA-Z-]*$', name):
        raise ValueError("Notebook命名必须为英文数字中划线组合,且首位必须是字母")
    return name.lower()




class Ssh(BaseModel):
    account: str
    password: str
    address: str = ""


class StatusItem(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    desc: str = None

class StatusItemOnlyDesc(BaseModel):
    desc: str = None


class UserStr(BaseModel):
    id: int
    username: str = None


class ProjectStr(BaseModel):
    id: Optional[int]
    name: Optional[str] = None


class Storage(BaseModel):
    name: Optional[str]
    id: int

class HookItem(BaseModel):
    storage: Storage
    path: str


class NotebookOp(BaseModel):
    action: int


class Creator(BaseModel):
    id: int
    username: str


class Project(BaseModel):
    id: int
    name: Optional[str]


class Image(BaseModel):
    name: str
    desc: Optional[str] = ""
    custom: Optional[bool] = False


class SourceItem(BaseModel):
    id: int
    name: str


class Grafana(BaseModel):
    cpu: str
    ram: str
    gpu: str
    vram: str


class NotebookList(BaseModel):
    id: int
    status: StatusItem
    name: str
    source: Optional[str]
    creator: Optional[UserStr]
    project: Optional[ProjectStr]
    image: Image
    url: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        return dt_to_string(dt, '%Y-%m-%d')


class NotebookCreate(BaseModel):
    name: str = Field(..., max_length=20)
    source: str
    project: Project
    image: Image
    custom: Optional[bool] = False
    hooks: List[HookItem] = []

    @validator('name')
    def notebook_name_validator(cls, name):
        return k8s_format(name)


class NotebookSimple(BaseModel):
    id: int
    name: str
    creator: Creator
    created_at: Optional[datetime]
    status: str
    project: Project
    updated_at: Optional[datetime]


class NotebookDetail(BaseModel):
    id: int
    name: str
    creator: Creator
    created_at: Optional[datetime]
    status: StatusItem
    url: Optional[str]
    project: Project
    image: Image
    source: str
    hooks: List[HookItem]
    updated_at: Optional[datetime]
    grafana: Optional[Grafana]
    server_ip: Optional[str]
    ssh: Optional[Ssh]


class NotebookEdit(BaseModel):
    name: Optional[str]
    source: Optional[str]
    project: Optional[Project]
    image: Optional[Image]
    hooks: Optional[List[HookItem]] = []

    @validator('name')
    def notebook_name_validator(cls, name):
        return k8s_format(name)


class EventItem(BaseModel):
    id: Optional[int]
    status: StatusItemOnlyDesc
    name: Optional[str] = ""
    time: Optional[datetime]


class EventCreate(BaseModel):
    name: str
    desc: str
    source_id: int
    source: Optional[str] = "NOTEBOOK"