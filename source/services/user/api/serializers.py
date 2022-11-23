# -*- coding: utf-8 -*-
"""
    >File    : serializers.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:12
"""
from pydantic import BaseModel


class LoginBody(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str
    token_type: str


class UserList(BaseModel):

    id: int
    username: str
    email: str
    role: int
