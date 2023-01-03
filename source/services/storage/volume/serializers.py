# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Optional, Union
import datetime

from pydantic import BaseModel, validator


class Owner(BaseModel):
    id: int
    username: str

class Creator(BaseModel):
    id: int
    username: str
    en_name: str

class Config(BaseModel):
    value: Optional[int] = 0
    size: int
    max: Optional[int]


class Project(BaseModel):
    id: int
    name: Optional[str] = None


class VolumeCreateReq(BaseModel):
    name: str
    project: Union[Project, None] = None
    config: Union[Config, None] = None
    owner: Union[Owner, None] = None

    @validator('name')
    def k8s_name_validator(cls, name):
        return name


class VolumeEditReq(BaseModel):
    project: Optional[Project] = None
    config: Optional[Config] = None
    owner: Optional[Owner] = None



# class VolumeResetReq(BaseModel):
#     id: int


class VolumeDetailRes(BaseModel):
    id: int
    name: str
    config: Config
    project: Project
    owner: Owner
    creator: Creator
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime] = None
