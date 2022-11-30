# -*- coding: utf-8 -*-
"""
    >File    : serializers.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:12
"""
from typing import Optional, List
from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import Field
from pydantic import EmailStr
from pydantic import validator
from pydantic import BaseModel
from datetime import datetime
from models import Role
from basic.utils.dt_format import dt_to_string
from role.serializers import RoleDetailSerializers
from auth.services import hash_password


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
    role: int = Field(..., ge=1, description='角色ID')
    project: Optional[List[int]] = []

    @validator('password')
    def set_password(cls, pwd):
        return hash_password(pwd)


class UserEdit(BaseModel):
    username: str = Field(None, max_length=80)
    password: str = Field(None, min_length=8, max_length=255)
    role:  Optional[int] = Field(None, description='角色ID')
    project: Optional[List[int]] = Field([], description='全量项目ID')

    @validator('password')
    def set_password(cls, pwd):
        return hash_password(pwd)


class UserItem(BaseModel):
    id: int
    username: str = None
    email: str = None


class UserList(UserItem):
    role: RoleDetailSerializers
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        return dt_to_string(dt)


class AdminUserListProject(BaseModel):
    id: int
    code: str
    name: str


class AdminUserList(UserList):
    projects: Optional[List[AdminUserListProject]] = None


class AccountInfo(UserList):
    project = []
    permissions = []

    class Config:
        orm_mode = True


class AccountEdit(BaseModel):
    username: str = Field(..., max_length=80)
    old_password: Optional[str] = Field(None, min_length=8, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=255)

    @validator('password')
    def set_password(cls, pwd):
        return hash_password(pwd) if pwd else None
