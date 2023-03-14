# -*- coding: utf-8 -*-
"""
    >File   : notebook.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/14 18:58
"""

from __future__ import annotations
import ormar
from basic.common.base_model import DateModel, GenericDateModel
from models import DB, META
import time

NOTEBOOK_STATUS_RUNNING = "RUNNING"
NOTEBOOK_STATUS_PENDING = "PENDING"
NOTEBOOK_STATUS_ERROR = "ERROR"
NOTEBOOK_STATUS_WAITING = "WAITING"
NOTEBOOK_STATUS_ON = "ON"


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
    memory: int = ormar.Integer(comment='存储容量G')
    gpu: int = ormar.Integer(comment='GPU数量')
    type: str = ormar.String(max_length=40, default='', comnet='CPU/GPU类型')
    desc: str = ormar.String(max_length=80, default='', comnet='备注')

    def get_str(self):
        if self.gpu:
            return f"GPU {self.gpu}*{self.type} {self.cpu}C {self.memory}G"
        else:
            return f"CPU {self.cpu}C {self.memory}G"

    def get_info(self):
        return {
            "id": self.id,
            "name": self.get_str(),
        }


class Notebook(GenericDateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_notebook"
        metadata = META
        database = DB
        orders_by = ['-id']

    name: str = ormar.String(max_length=20, comnet='名称')
    url: str = ormar.String(max_length=160, comnet='url地址', nullable=True)
    status: Status = ormar.ForeignKey(Status, related_name='notebook_status')
    cpu: int = ormar.Integer(comment='CPU数量')
    memory: int = ormar.Integer(comment='存储容量G')
    gpu: int = ormar.Integer(comment='GPU数量')
    type: str = ormar.String(max_length=40, default='', comnet='CPU/GPU类型')
    image: str = ormar.String(max_length=150, comment='镜像名称')
    custom: bool = ormar.Boolean(default=False)
    storage: str = ormar.JSON(comment='存储信息')
    k8s_info: str = ormar.JSON(comment='集群信息')
    server_ip: str = ormar.String(max_length=20, comment='所在的node name', nullable=True)
    host_ip: str = ormar.String(max_length=20, comment='所在的node ip', nullable=True)
    pod_ip: str = ormar.String(max_length=20, comment='所在的node ip', nullable=True)

    @property
    def start_time_timestamp(self):
        return time.mktime(self.started_at.timetuple()) if self.started_at else time.time()

    @property
    def ended_time_timestamp(self):
        return time.mktime(self.ended_at.timetuple()) if self.ended_at else time.time()

    def cpu_url(self, common: str):
        return f"{common}orgId=1&var-namespace={self.namespace_name()}&var-cluster=&var-job={self.pod_name()}&panelId=4&from={self.start_time_timestamp}&to={self.ended_time_timestamp}"

    def gpu_url(self, common: str):
        if self.gpu > 0:
            return f"{common}orgId=1&var-namespace={self.namespace_name()}&var-cluster=&var-job={self.pod_name()}&panelId=8&from={self.start_time_timestamp}&to={self.ended_time_timestamp}"
        else:
            return ""

    def ram_url(self, common: str):
        return f"{common}orgId=1&var-namespace={self.namespace_name()}&var-cluster=&var-job={self.pod_name()}&panelId=6&from={self.start_time_timestamp}&to={self.ended_time_timestamp}"

    def vram_url(self, common: str):
        if self.gpu > 0:
            return f"{common}orgId=1&var-namespace={self.namespace_name()}&var-cluster=&var-job={self.pod_name()}&panelId=12&from={self.start_time_timestamp}&to={self.ended_time_timestamp}"
        else:
            return ""

    def namespace_name(self):
        return f"{self.k8s_info.get('namespace')}"

    def pod_name(self):
        return f"{self.k8s_info.get('name')}-0"

    def get_source(self):
        if self.gpu:
            return f"GPU {self.gpu}*{self.type} {self.cpu}C {self.memory}G"
        else:
            return f"CPU {self.cpu}C {self.memory}G"

    def get_dict(self):
        note_config = [y['storage']['config'] for y in self.storage]
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
            status=self.status.name,
            cpu=self.cpu,
            memory=self.memory,
            gpu=self.gpu,
            namespace_name=self.namespace_name(),
            pod_name=self.pod_name(),
            creator=dict(
                id=int(self.created_by_id),
                username=self.created_by,
            ),
            project=dict(
                id=int(self.project_by_id),
                name=self.project_by,
            ),
            volume_ids=[y['storage']['id'] for y in self.storage],
            storage_value=sum([conf['value'] for conf in note_config]),
            storage_size=sum([conf['size'] for conf in note_config]),
        )

    @classmethod
    def compare_status_and_update(cls, nb: Notebook, status: str, status_dic):
        if status == NOTEBOOK_STATUS_ON:
            nb.status = status_dic['running']
        elif status == NOTEBOOK_STATUS_ERROR:
            nb.status = status_dic['error']
        elif status == NOTEBOOK_STATUS_PENDING:
            nb.status = status_dic["pending"]
        elif status == NOTEBOOK_STATUS_RUNNING:
            nb.status = status_dic['start']

    @classmethod
    async def self_project(cls, _id: int):
        return await cls.objects.filter(cls.project_by_id == _id).count()

    @classmethod
    async def self_project_and_self_view(cls, project_id: int, self_id: int):
        return await cls.objects.filter((cls.project_by_id == project_id) & (cls.created_by_id == self_id)).count()

    @classmethod
    async def project_list_by_ip(cls, _ip: int):
        return await cls.objects.all(cls.server_ip == _ip, status__in=[4, 11])
