# -*- coding: utf-8 -*-

import ormar
from basic.common.base_model import DateModel
from models import DB, META


class Event(DateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_event"
        metadata = META
        database = DB
        orders_by = ['-id']

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, comnet='事件名称')
    desc: str = ormar.String(max_length=200, default='', comment='事件描述')
    status: str = ormar.String(max_length=30, default="", comment="状态")
    source: str = ormar.String(max_length=30, default="", comment="事件来源")
    source_id: int = ormar.Integer()


    def gen_pagation_event(self):
        return {
            "id": self.id,
            "status": self.status,
            "name": self.name,
            "time": self.created_at,
        }