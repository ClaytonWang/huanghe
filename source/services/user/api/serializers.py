# -*- coding: utf-8 -*-
"""
    >File    : serializers.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:12
"""
from pydantic import BaseModel


class LoginBodySerializers(BaseModel):
    email: str
    password: str


class TokenSerializers(BaseModel):
    token: str
    token_type: str


class UserListSerializers(BaseModel):

    id: int
    username: str
    email: str
    role: int
