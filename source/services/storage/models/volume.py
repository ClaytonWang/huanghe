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
from datetime import datetime



class Volume(DateAuditModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_volume"
        metadata = META
        database = DB
        orders_by = ['-id']

    name: str = ormar.String(max_length=80, comment='存储盘名称')
    owner: str = ormar.String(max_length=12, nullable=True, comment='持有人')
    value: int = ormar.Integer(minimum=0, maximum=99999, default=0, comment="当前容量")
    size: int = ormar.Integer(minimum=0, maximum=99999, comment="当前容量")
    username: str = ormar.String(max_length=12, nullable=True, comment="创建人")
    delete_time: datetime = ormar.DateTime(default=None, nullable=True, comment='删除日期')

    def __repr__(self):
        return f'{self.username}_{self.name}'
