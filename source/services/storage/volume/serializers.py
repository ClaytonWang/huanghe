# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Optional, Union
import datetime

from pydantic import BaseModel, validator


class Owner(BaseModel):
    id: int
    name: str


class ProjectStr(BaseModel):
    id: str
    name: Optional[str] = None


class OwnerStr(BaseModel):
    id: str
    name: str


class Config(BaseModel):
    value: Optional[int] = 0
    size: int


class Project(BaseModel):
    id: int
    name: Optional[str] = None


class VolumeCreateReq(BaseModel):
    name: str
    project: Union[ProjectStr, None] = None
    config: Union[Config, None] = None
    owner: Union[Owner, None] = None

    @validator('name')
    def k8s_name_validator(cls, name):
        return name


class VolumeEditReq(BaseModel):
    project: Optional[ProjectStr] = None
    config: Optional[Config] = None
    owner: Optional[OwnerStr] = None



# class VolumeResetReq(BaseModel):
#     id: int


class VolumeDetailRes(BaseModel):
    id: str
    name: str
    config: Config
    project: ProjectStr
    owner: OwnerStr
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime] = None
