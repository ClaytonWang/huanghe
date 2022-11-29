# -*- coding: utf-8 -*-
"""
    >File    : serializers.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/29 16:37
"""
from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str
    token_type: str
