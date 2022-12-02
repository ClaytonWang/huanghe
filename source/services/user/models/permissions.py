# -*- coding: utf-8 -*-
"""
    >File    : permissions.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 08:34
"""
import ormar
from enum import Enum
from typing import Optional, List
from basic.common.base_model import DateAuditModel
from models import DB, META
from models.user import Role, User
from models.project import Project


class PmsOpt(int, Enum):
    project_edit: 1    # 编辑
    project_readonly: 2   # 查看


class PmsCategory(str, Enum):
    project: 'project'


class Permissions(DateAuditModel):
    """
    模块菜单权限

    层级权限关联角色，

    非层级权限关联用户
    """
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_permissions"
        metadata = META
        database = DB

    # 4位一个层级，最多5层
    code: str = ormar.String(max_length=20, unique=True)

    name: str = ormar.String(max_length=30, comment='模块/菜单/操作标题')
    value: str = ormar.String(max_length=50, nullable=True, comment='描述')
    uri: str = ormar.JSON(nullable=True, comment='资源（预留）')

    role: Optional[List[Role]] = ormar.ManyToMany(Role)
    user: Optional[List[User]] = ormar.ManyToMany(User)
    project: Optional[List[Project]] = ormar.ManyToMany(Project)

    def __repr__(self):
        return f'{self.name}__{self.code}'
