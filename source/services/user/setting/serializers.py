# -*- coding: utf-8 -*-
"""
    >File    : serializers.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/29 19:35
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class ProjectSetUser(BaseModel):
    user: int = Field(..., ge=1, description='需要关联的用户ID')
    project: int = Field(..., ge=1, description='项目ID')
    permissions: List[int] = Field(..., description='权限列表')
