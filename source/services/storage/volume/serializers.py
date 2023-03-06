# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Optional, Union
from fastapi import HTTPException, status
import datetime
import re

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
    config: Union[Config, None] = None
    owner: Union[Owner, None] = None

    @validator('name')
    def k8s_name_validator(cls, name):
        if not name or not re.match('^[a-z][0-9a-z-]*$', name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='存储命名必须为小写英文字母数字中划线组合,且首位必须是字母')
        return name


class VolumeEditReq(BaseModel):
    config: Optional[Config] = None
    owner: Optional[Owner] = None


class VolumeDetailRes(BaseModel):
    id: int
    name: str
    config: Config
    owner: Owner
    creator: Creator
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime] = None
