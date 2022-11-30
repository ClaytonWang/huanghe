# -*- coding: utf-8 -*-
"""
    >File    : users.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/11 09:27
"""

import ormar
from typing import Optional
from basic.common.base_model import DateModel
from basic.common.base_model import DateAuditModel
from models import DB, META


class Role(DateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_role"
        metadata = META
        database = DB
        orders_by = ['-id']

    id: int = ormar.Integer(primary_key=True)
    name = ormar.String(max_length=30, comnet='角色名', unique=True)
    value = ormar.String(max_length=30, default='', nullable=True, comment='说明')

    def __repr__(self):
        return f'{self.name}_{self.vlaue}'


class User(DateAuditModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_user"
        metadata = META
        database = DB
        orders_by = ['-id']

    username: str = ormar.String(max_length=80, comment='用户名')
    email: str = ormar.String(max_length=80, comment='邮箱', unique=True, )
    password: str = ormar.String(max_length=255, comment='密码')
    first_name: str = ormar.String(max_length=20, nullable=True)
    last_name: str = ormar.String(max_length=60, nullable=True)
    phone: str = ormar.String(max_length=12, nullable=True)
    is_delete: bool = ormar.Boolean(default=False, comment='是否删除')
    role: Optional[Role] = ormar.ForeignKey(to=Role, related_name='users')

    def __repr__(self):
        return f'{self.username}_{self.email}'
