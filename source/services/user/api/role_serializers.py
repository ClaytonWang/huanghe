# -*- coding: utf-8 -*-
"""
    >File    : role_serializers.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 09:04
"""
from pydantic import BaseModel


class RoleDetailSerializers(BaseModel):
    id: int
    name: str
    text: str
