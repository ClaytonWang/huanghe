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


class PmsOpt(int, Enum):
    project_edit: 1    # 编辑
    project_readonly: 2   # 查看


class PmsCategory(str, Enum):
    project: 'project'


class Permissions(DateAuditModel):
    """
    模块菜单权限
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
    project: str = ormar.String(max_length=30, nullable=True, comment='项目（预留扩展）')

    role: Optional[List[Role]] = ormar.ManyToMany(Role)
    user: Optional[List[User]] = ormar.ManyToMany(User)

    def __repr__(self):
        return f'{self.name}__{self.code}'


class OperationPms(DateAuditModel):
    """
    功能操作权限
    """
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_pms_operation"
        metadata = META
        database = DB

    code: str = ormar.Enum(enum_class=PmsOpt, unique=True, comment='权限编码，全局唯一')
    name: str = ormar.String(max_length=30, comment='权限英文名（不能模块下可重复')
    value: str = ormar.String(max_length=50, nullable=True, comment='描述')
    category: str = ormar.Enum(enum_class=PmsCategory, max_length=30, comment='数据分类')
    category_pk_id: str = ormar.BigInteger(comment='数据分类主键ID')

    role: Optional[List[Role]] = ormar.ManyToMany(Role)
    user: Optional[List[User]] = ormar.ManyToMany(User)

    def __repr__(self):
        return f'f{self.category}__{self.name}__{self.code}'
