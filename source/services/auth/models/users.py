# -*- coding: utf-8 -*-
"""
    >File    : users.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/11 09:27
"""

import ormar
from .base_model import DateFieldsModel, DateFieldsMixins


class User(DateFieldsModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=255, nullable=False)
    email: str = ormar.String(max_length=255, nullable=True)
    password: str = ormar.String(max_length=255, pydantic_only=True)
    first_name: str = ormar.String(max_length=255, nullable=True)
    last_name: str = ormar.String(max_length=255, nullable=True)
    phone: str = ormar.String(max_length=12, nullable=True)
    category: str = ormar.String(max_length=255, nullable=True)

