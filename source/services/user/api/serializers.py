# -*- coding: utf-8 -*-
"""
    >File    : serializers.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:12
"""
from typing import Optional, List
from pydantic import Field
from pydantic import EmailStr
from pydantic import validator
from pydantic import BaseModel
from datetime import datetime
from basic.utils.dt_format import dt_to_string
from role.serializers import RoleDetailSerializers
from api.services import hash_password


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str
    token_type: str


class UserCreate(BaseModel):
    username: str = Field(..., max_length=80)
    password: str = Field(..., min_length=8, max_length=255)
    email: EmailStr
    role: int
    project: int = Optional[int]

    @validator('password')
    def set_password(cls, pwd):
        return hash_password(pwd)


class UserEdit(BaseModel):
    username: str = Field(None, max_length=80)
    password: str = Field(None, min_length=8, max_length=255)
    role:  Optional[int] = None
    project: Optional[List[int]] = None

    @validator('password')
    def set_password(cls, pwd):
        return hash_password(pwd)


class UserList(BaseModel):
    id: int
    username: str
    email: str
    role: RoleDetailSerializers
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        return dt_to_string(dt)


class AccountInfo(UserList):
    project = []
    permissions = []

    class Config:
        orm_mode=True
