# -*- coding: utf-8 -*-
"""
    >File   : serializers.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/15 10:21
"""
import re
from datetime import datetime
from fastapi import HTTPException, status
from typing import Optional, List, Union

from pydantic import BaseModel, Field
from pydantic import validator

from basic.utils.dt_format import dt_to_string


def k8s_format(name):
    if not name or not re.match('^[a-z][0-9a-z-]*$', name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Job命名必须为小写英文字母数字中划线组合,且首位必须是字母')
    return name.lower()


class StatusItem(BaseModel):
    code: str = None
    name: str = None
    desc: str = None


class UserStr(BaseModel):
    id: int
    username: str = None


class StartMode(BaseModel):
    id: int
    name: Optional[str]


class ModeRes(BaseModel):
    id: int
    max_nodes: str
    name: str


class Grafana(BaseModel):
    cpu: str
    ram: str
    gpu: str
    vram: str


class ProjectStr(BaseModel):
    id: int
    name: Optional[str] = None


class Storage(BaseModel):
    name: Optional[str]
    id: int


class HookItem(BaseModel):
    storage: Storage
    path: str


class JobOpReq(BaseModel):
    action: int

    @validator("action")
    def validate_bad_words(cls, action: int):
        if action not in [0, 1]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='操作错误')
        return action


class JobOpRes(BaseModel):
    id: int
    
    
class Url(BaseModel):
    name: str
    url: str


class Creator(BaseModel):
    id: str
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


class JobSimple(BaseModel):
    id: int
    status: str
    name: str
    creator: Optional[UserStr]
    project: Optional[ProjectStr]
    created_at: Union[datetime, str, None]
    updated_at: Union[datetime, str, None]
    mode: str
    volume_ids: List[int]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        if isinstance(dt, str):
            return dt
        return dt_to_string(dt, '%Y-%m-%d')


class JobList(BaseModel):
    id: int
    status: StatusItem
    name: str
    source: Optional[str]
    creator: Optional[UserStr]
    project: Optional[ProjectStr]
    image: Image
    url: Optional[List[Url]]
    created_at: Union[datetime, str, None]
    updated_at: Union[datetime, str, None]
    mode: str

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        if isinstance(dt, str):
            return dt
        return dt_to_string(dt, '%Y-%m-%d')


class JobCreate(BaseModel):
    name: str = Field(..., max_length=20)
    project: Project
    source: str
    start_command: Optional[str]
    mode: str
    image: Image
    work_dir: Optional[str]
    hooks: List[HookItem] = []
    start_mode: Optional[StartMode]
    nodes: Optional[int] = 1

    @validator('name')
    def job_name_validator(cls, name):
        return k8s_format(name)


class JobDetail(BaseModel):
    id: int
    name: str
    creator: Creator
    created_at: Union[datetime, str, None]
    status: StatusItem
    project: Project
    image: Image
    source: str = None
    hooks: List[HookItem]
    updated_at: Union[datetime, str, None]
    mode: str
    url: Optional[List[Url]]
    grafana: Optional[Grafana]
    logging_url: Optional[str]
    start_command: Optional[str]
    work_dir: Optional[str]
    nodes: Optional[int]
    start_mode: Optional[StartMode]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        if isinstance(dt, str):
            return dt
        return dt_to_string(dt, '%Y-%m-%d')


class JobEditReq(BaseModel):
    project: Project
    mode: str
    start_command: Optional[str]
    image: Image
    work_dir: Optional[str]
    hooks: List[HookItem] = []
    source: str
    start_mode: Optional[StartMode]
    nodes: Optional[int]


class JobEditRes(BaseModel):
    id: int


class StatusItemOnlyDesc(BaseModel):
    desc: str = None


class JobStatusUpdateReq(BaseModel):
    status: str
    server_ip: Optional[str]


class JobStatusUpdateRes(BaseModel):
    id: int


class EventItem(BaseModel):
    id: Optional[int]
    status: StatusItemOnlyDesc
    name: Optional[str] = ""
    time: Optional[datetime]


class EventCreate(BaseModel):
    name: str
    desc: str
    source_id: int
    source: Optional[str] = "VCJOB"
