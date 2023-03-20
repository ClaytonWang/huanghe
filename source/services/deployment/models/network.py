# -*- coding: utf-8 -*-
"""
    >File   : network.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/16 19:08
"""
from __future__ import annotations

import datetime
import time

import ormar
from basic.config.job_management import WEBKUBECTL_URL
from basic.common.base_model import GenericDateModel
from basic.common.status_cache import Status
from basic.common.initdb import DB, META


class Service(GenericDateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_service"
        metadata = META
        database = DB
        orders_by = ['-id']

    name: str = ormar.String(max_length=20, comment='名称')
    private_url: str = ormar.JSON(comment='内部域名')
    deployment_id: int = ormar.Integer(comment='负载')
    cluster_ip: str = ormar.String(max_length=20, comment='访问地址')
    port: int = ormar.Integer(comment='端口')


class Ingress(GenericDateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_ingress"
        metadata = META
        database = DB
        orders_by = ['-id']

    name: str = ormar.String(max_length=20, comment='名称')
    private_url: str = ormar.JSON(comment='内部域名')
    deployment_id: int = ormar.Integer(comment='负载')
    cluster_ip: str = ormar.String(max_length=20, comment='访问地址')
    port: int = ormar.Integer(comment='端口')
