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
from permissions.serializers import PmsSerializers
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
    role: str = Field(..., description='角色名称')
    project: Optional[List[int]] = []

    @validator('password')
    def set_password(cls, pwd):
        return hash_password(pwd)


class UserEdit(BaseModel):
    username: str = Field(None, max_length=80)
    password: str = Field(None, min_length=8, max_length=255)
    role:  Optional[str] = Field(None, description='角色名')
    projects: Optional[List[int]] = Field([], description='全量项目ID')

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
    """
    项目负责人里不一定会有项目，默认设置空
    """
    id: int = None
    code: str = None
    name: str = None


class AdminUserList(UserList):
    projects: Optional[List[AdminUserListProject]] = None


class OwnerUserList(UserItem):
    project: Optional[AdminUserListProject] = None
    permissions: Optional[List[PmsSerializers]] = None
    user_id: int


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
