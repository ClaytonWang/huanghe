# -*- coding: utf-8 -*-
"""
    >File   : serializers.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/15 10:21
"""
import re
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic import validator

from basic.utils.dt_format import dt_to_string


def k8s_format(name):
    if not name or not re.match('^[a-zA-Z][0-9a-zA-Z-]*$', name):
        raise ValueError("Job命名必须为英文数字中划线组合,且首位必须是字母")
    return name.lower()


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


class Storage(BaseModel):
    name: Optional[str]
    id: str


class HookItem(BaseModel):
    storage: Storage
    path: str


class JobOp(BaseModel):
    action: int


class Creator(BaseModel):
    id: str
    username: str


class Project(BaseModel):
    id: str
    name: Optional[str]


class Image(BaseModel):
    name: str
    desc: Optional[str] = ""
    custom: Optional[bool] = False


class SourceItem(BaseModel):
    id: int
    name: str


class JobList(BaseModel):
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
    task_model_name: str

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        return dt_to_string(dt, '%Y-%m-%d')


class JobCreate(BaseModel):
    name: str = Field(..., max_length=20)
    project: Project
    source_id: int
    task_model: int
    start_command: str
    image_type: int
    image_name: str = Field(..., max_length=100)
    work_dir: str

    hooks: List[HookItem] = []

    @validator('name')
    def job_name_validator(cls, name):
        return k8s_format(name)


class JobDetail(BaseModel):
    id: int
    name: str
    creator: Creator
    created_at: Optional[datetime]
    status: StatusItem
    project: Project
    image_type: int
    image_name: str
    source: str = None
    hooks: List[HookItem]
    updated_at: Optional[datetime]
    task_model_name: str
    task_model: int

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        return dt_to_string(dt, '%Y-%m-%d')

class JobEdit(BaseModel):
    project: Project
    task_model: int
    start_command: str
    image_type: int
    image_name: str = Field(..., max_length=100)
    work_dir: str
    hooks: List[HookItem] = []
    source_id: int
