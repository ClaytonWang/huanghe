# -*- coding: utf-8 -*-
"""
    >File   : notebook.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/14 18:58
"""

import ormar
from basic.common.base_model import DateModel
from models import DB, META


class Status(ormar.Model):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_status"
        metadata = META
        database = DB
        orders_by = ['-id']

    id: int = ormar.Integer(primary_key=True)
    code: str = ormar.String(max_length=20, comnet='状态码', unique=True)
    name: str = ormar.String(max_length=20, comnet='名称', unique=True)
    desc: str = ormar.String(max_length=40, comnet='描述')


class Source(DateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_source"
        metadata = META
        database = DB
        orders_by = ['id']

    id: int = ormar.Integer(primary_key=True)
    cpu: int = ormar.Integer(comment='CPU数量')
    cpu_type: str = ormar.String(max_length=20, comnet='CPU类型', nullable=True)
    memory: int = ormar.Integer(comment='存储容量G')
    gpu: int = ormar.Integer(comment='GPU数量')
    gpu_type: str = ormar.String(max_length=20, default='A100', comnet='GPU类型')
    desc: str = ormar.String(max_length=80, default='', comnet='备注')

    def get_dict(self):
        return {
            "id": self.id,
            "cpu": self.cpu,
            "memory": self.memory,
            "gpu": self.gpu,
        }

    def get_str(self):
        return f"{self.gpu}*{self.gpu_type} {self.cpu}C {self.memory}G"


class Notebook(DateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_notebook"
        metadata = META
        database = DB
        orders_by = ['-id']

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=20, comnet='名称', unique=True)
    status: Status = ormar.ForeignKey(Status, related_name='notebook_status')
    source = ormar.ForeignKey(Source, related_name='notebook_source')

    creator_id: int = ormar.Integer(comment='创建者id')
    project_id: int = ormar.Integer(comment='项目id')
    image_id: int = ormar.Integer(comment='镜像id')

    # 对多个volume如何处理
    storage: str = ormar.JSON(comment='存储信息')

    # def __repr__(self):
    #     return f'{self.name}_{self.value}'
