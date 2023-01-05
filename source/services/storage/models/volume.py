# -*- coding: utf-8 -*-
"""
    >File    : users.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/11 09:27
"""
from __future__ import annotations

import datetime
from fastapi import HTTPException, status
import ormar
from basic.common.base_model import GenericDateModel
from models import DB, META
from volume.serializers import VolumeCreateReq, VolumeEditReq
from basic.middleware.account_getter import AccountGetter, ProjectGetter, ADMIN


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
    max: int = ormar.Integer(minimum=0, maximum=9999999, default=1024, comment="当前限制")

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
                "max": self.max,
            },
            "project": {
                "id": self.project_by_id,
                "name": self.project_by,
            },
            "owner": {
                "id": self.owner_by_id,
                "username": self.owner_by,
            },
            "creator": {
                "id": self.created_by_id,
                "username": self.created_by,
                "en_name": self.create_en_by,
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
            "create_en_by": ag.en_name,
            "project_en_by": pg.en_name,
            "created_by": ag.username,
            "updated_by": ag.username,
            "project_by": pg.name,
            "name": vcr.name,
            "owner_by": vcr.owner.username,
            "owner_by_id": vcr.owner.id,
            "size": vcr.config.size,
            "max": 9999999 if ag.role.name == ADMIN else 1024
        }

    @classmethod
    async def undeleted_volumes(cls):
        return cls.objects.filter(
            (cls.deleted_at == None) | (cls.deleted_at >= datetime.datetime.now() - datetime.timedelta(days=7)))

    @classmethod
    async def undeleted_self_project_volumes(cls, project_ids):
        return cls.objects.filter(
            (cls.project_by_id << project_ids) & ((cls.deleted_at == None) | (
                        cls.deleted_at >= datetime.datetime.now() - datetime.timedelta(days=7)))
        )

    @classmethod
    async def get_by_id(cls, _id) -> Volume:
        v = await cls.objects.get(id=_id)
        return v

    @classmethod
    async def get_by_self_id(cls, _id, owner_id) -> Volume:
        v = await cls.objects.get_or_none(id=_id, owner_by_id=owner_id)
        if not v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'该盘的所属人不为当前用户')
        return v

    @classmethod
    async def set_deleted(cls, _id, owner_id) -> Volume:
        v = await cls.get_by_self_id(_id, owner_id)
        await v.update(**{"deleted_at": datetime.datetime.now()})
        return v

    @classmethod
    async def cancel_deleted(cls, _id) -> Volume:
        v = await cls.get_by_id(_id)
        await v.update(**{"deleted_at": None})
        return v
