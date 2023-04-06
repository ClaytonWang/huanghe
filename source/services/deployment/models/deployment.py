# -*- coding: utf-8 -*-
"""
    >File   : deployment.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/16 11:17
"""
from __future__ import annotations

import datetime
import time

import ormar
from basic.common.base_model import GenericDateModel
from basic.common.status_cache import Status
from basic.common.initdb import DB, META



# 状态


class Deployment(GenericDateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_deployment"
        metadata = META
        database = DB
        orders_by = ['-id']

    name: str = ormar.String(max_length=20, comment='名称')
    private_ip: str = ormar.String(max_length=20, comment='私网IP', nullable=True)
    public_ip: str = ormar.String(max_length=20, comment='公网IP', nullable=True)
    image: str = ormar.String(max_length=150, comment='镜像名称')
    status: Status = ormar.ForeignKey(Status, related_name='deployment_status')
    cpu: int = ormar.Integer(comment='CPU数量')
    memory: int = ormar.Integer(comment='存储容量G')
    gpu: int = ormar.Integer(comment='GPU数量')
    type: str = ormar.String(max_length=40, default='', comment='CPU/GPU类型')

    @property
    def is_public(self):
        return True if self.public_ip else False

    @classmethod
    async def all_deployments(cls):
        return cls.objects.filter()

    @classmethod
    async def self_view(cls, _id: int):
        return cls.objects.filter(cls.created_by_id == _id)

    @classmethod
    async def self_project(cls, _id: int):
        return await cls.objects.filter(cls.project_by_id == _id).count()

    @classmethod
    async def self_project_and_self_view(cls, project_id: int, self_id: int):
        return await cls.objects.filter((cls.project_by_id == project_id) & (cls.created_by_id == self_id)).count()

    @classmethod
    async def get_deployment_related_status_by_pk(cls, pk):
        return await Deployment.objects.select_related(['status']).get(pk=pk)


    @property
    def start_time_timestamp(self):
        return int(time.mktime(self.started_at.utctimetuple())) if self.started_at \
            else int(time.mktime(datetime.datetime.utcnow().utctimetuple()))

    @property
    def ended_time_timestamp(self):
        return int(time.mktime(self.ended_at.utctimetuple())) if self.ended_at \
            else int(time.mktime(datetime.datetime.utcnow().utctimetuple()))


    @property
    def source(self):
        if self.gpu:
            return f"GPU {self.gpu}*{self.type} {self.cpu}C {self.memory}G"
        else:
            return f"CPU {self.cpu}C {self.memory}G"


    def gen_deployment_pagation_response(self):
        return {
            "id": self.id,
            "status": {"code": self.status.code,
                       "name": self.status.name,
                       "desc": self.status.desc, },
            "name": self.name,
            "source": self.source,
            "creator": {"id": self.created_by_id,
                        "username": self.created_by, },
            "project": {"id": self.project_by_id,
                        "name": self.project_by, },
            "image": {"name": self.image,
                      "custom": True, },
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "urls": [
                {"type": "public", "address": self.public_ip},
                {"type": "private", "address": self.private_ip},
            ] if self.public_ip else [
                {"type": "private", "address": self.private_ip},
            ],
            "is_public": self.is_public,
        }


    def gen_deployment_detail_response(self):
        return {
            "id": self.id,
            "status": {"code": self.status.code,
                       "name": self.status.name,
                       "desc": self.status.desc, },
            "name": self.name,
            "creator": {"id": self.created_by_id,
                        "username": self.created_by, },
            "project": {"id": self.project_by_id,
                        "name": self.project_by, },
            "image": {"name": self.image,
                      "custom": True, },
            "source": self.source,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
            "urls": [
                {"type": "public", "address": self.public_ip},
                {"type": "private", "address": self.private_ip},
            ],
            "is_public": self.is_public,
        }


