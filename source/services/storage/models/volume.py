# -*- coding: utf-8 -*-
"""
    >File    : users.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/11 09:27
"""
from __future__ import annotations

import datetime

import ormar
from basic.common.base_model import GenericDateModel
from models import DB, META
from volume.serializers import VolumeCreateReq, VolumeEditReq
from basic.middleware.account_getter import AccountGetter, ProjectGetter


class Volume(GenericDateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_volume"
        metadata = META
        database = DB
        orders_by = ['-id']

    name: str = ormar.String(max_length=80, comment='存储盘名称')
    owner_by: str = ormar.String(max_length=12, nullable=True, comment='持有者')
    owner_by_id: int = ormar.Integer(comment='持有者id', nullable=True)
    value: int = ormar.Integer(minimum=0, maximum=99999, default=0, comment="当前容量")
    size: int = ormar.Integer(minimum=0, maximum=99999, comment="最大容量")

    # def __repr__(self):
    #     return f'{self.username}_{self.name}'

    def __gt__(self, other: Volume):
        return self.size > other.size

    def gen_volume_pagation_response(self):
        return {
            "id": self.id,
            "name": self.name,
            "config": {
                "value": self.value,
                "size": self.size,
            },
            "project": {
                "id": self.project_by_id,
                "name": self.project_by,
            },
            "owner": {
                "id": self.owner_by_id,
                "name": self.owner_by,
            },
            "created_at": self.created_at,
            "deleted_at": self.deleted_at,
        }

    @staticmethod
    def gen_create_dict(ag: AccountGetter, pg: ProjectGetter, vcr: VolumeCreateReq):
        return {
            "created_by_id": ag.id,
            "updated_by_id": ag.id,
            "project_by_id": pg.id,
            "created_by": ag.username,
            "updated_by": ag.username,
            "project_by": pg.name,
            "name": vcr.name,
            "owner_by": vcr.owner.name,
            "owner_by_id": vcr.owner.id,
            "size": vcr.config.size,
        }

    @staticmethod
    def gen_edit_dict(ver: VolumeEditReq):
        d = {}
        if ver.project:
            d.update({"project_by_id": ver.project.id})
        if ver.size:
            d.update({"size": ver.size})
        if ver.owner:
            d.update({"owner_by": ver.owner.name,
                      "owner_by_id": ver.owner.id})
        return d

    @classmethod
    async def undeleted_volumes(cls):
        return cls.objects.filter(
            (cls.deleted_at == None) | (cls.deleted_at >= datetime.datetime.now() - datetime.timedelta(days=7)))

    @classmethod
    async def undeleted_self_volumes(cls, owner_id):
        return cls.objects.filter(
            (cls.owner_by_id == owner_id) & ((cls.deleted_at == None) | (
                        cls.deleted_at >= datetime.datetime.now() - datetime.timedelta(days=7)))
        )

    @classmethod
    async def get_by_id(cls, _id) -> Volume:
        v = await cls.objects.get(id=_id)
        return v

    @classmethod
    async def set_deleted(cls, _id) -> Volume:
        v = await cls.get_by_id(_id)
        await v.update(**{"deleted_at": datetime.datetime.now()})
        return v

    @classmethod
    async def cancel_deleted(cls, _id) -> Volume:
        v = await cls.get_by_id(_id)
        await v.update(**{"deleted_at": None})
        return v

    @classmethod
    async def compare_with_old(cls, _id, ver: VolumeEditReq):
        v = await cls.get_by_id(_id)
        d = {}
        if ver.project.id and v.project_by_id != ver.project.id:
            d.update({"project_by_id": ver.project.id,
                      "project_by": ver.project.name})
        if ver.config.size and ver.config.size > v.size:
            d.update({"size": ver.config.size})
        if ver.owner and ver.owner.id != v.owner_by_id:
            d.update({"owner_by": ver.owner.name,
                      "owner_by_id": ver.owner.id})
        await v.update(**d)
