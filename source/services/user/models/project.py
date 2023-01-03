# -*- coding: utf-8 -*-
"""
    >File    : project.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/28 19:20
"""
import ormar
from typing import Optional, List
from basic.common.base_model import DateAuditModel
from models import DB, META, User


class Project(DateAuditModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_project"
        metadata = META
        database = DB
        orders_by = ['-id']
        constraints = [ormar.IndexColumns('id', )]

    code: str = ormar.String(max_length=80, comment='项目Code', unique=True)
    name: str = ormar.String(max_length=80, comment='项目名称', unique=True, )
    en_name: str = ormar.String(max_length=40, comment='项目英文名', unique=True)
    owner: Optional[User] = ormar.ForeignKey(to=User, related_name='project_user')

    member: Optional[List[User]] = ormar.ManyToMany(to=User)

    def __repr__(self):
        return f'{self.owner}_{self.code}_{self.name}'
