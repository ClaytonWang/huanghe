# -*- coding: utf-8 -*-
"""
    >File    : permissions.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 08:34
"""
import ormar
from typing import Optional, List
from basic.common.base_model import DateAuditModel
from models import DB, META
from models.user import Role, User


class Permissions(DateAuditModel):
    """
    """
    # 4位一个层级，最多5层
    id: int = ormar.Integer(primary_key=True)
    code: str = ormar.String(max_length=20, unique=True)

    name: str = ormar.String(max_length=30, verbose_name='模块/菜单/操作标题')
    text: str = ormar.String(max_length=50, blank=True, null=True, verbose_name='中文')

    role: Optional[List[Role]] = ormar.ManyToMany(Role)
    user: Optional[List[User]] = ormar.ManyToMany(User)

    class Meta(ormar.ModelMeta):
        tablename: str = "user_permissions"
        metadata = META
        database = DB
