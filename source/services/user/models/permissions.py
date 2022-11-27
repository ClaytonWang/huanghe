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
    class Meta(ormar.ModelMeta):
        tablename: str = "user_permissions"
        metadata = META
        database = DB

    # 4位一个层级，最多5层
    code: str = ormar.String(max_length=20, unique=True)

    name: str = ormar.String(max_length=30, comment='模块/菜单/操作标题')
    value: str = ormar.String(max_length=50, nullable=True, comment='描述')
    uri: str = ormar.JSON(nullable=True, comment='资源（预留）')
    project: str = ormar.String(max_length=30, nullable=True, comment='项目（预留扩展）')

    role: Optional[List[Role]] = ormar.ManyToMany(Role)
    user: Optional[List[User]] = ormar.ManyToMany(User)

    def __repr__(self):
        return f'{self.name}__{self.code}'
