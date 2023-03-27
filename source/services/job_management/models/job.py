# -*- coding: utf-8 -*-
"""
    >File   : job.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/14 18:58
"""

from __future__ import annotations

import datetime
import time

import ormar
from basic.config.job_management import WEBKUBECTL_URL
from basic.common.base_model import GenericDateModel
from basic.common.status_cache import Status
from services.job_management.models.mode import Mode
from basic.common.initdb import DB, META

# 状态
# JOB_STATUS_RUNNING = "running"  # 已启动(运行中)
# JOB_STATUS_STOP = "stop"  # 停止中
# JOB_STATUS_START_FAIL = "start_fail"  # 启动失败
# JOB_STATUS_RUN_FAIL = "run_fail"  # 运行失败
# JOB_STATUS_STOP_FAIL = "stop_fail"  # 停止失败
# JOB_STATUS_ON = "on"  # 已完成
# JOB_STATUS_STOPPED = "stopped"  # 已停止

JOB_STATUS_PENDING = "Pending"
JOB_STATUS_COMPLETING = "Completing"
JOB_STATUS_COMPLETED = "Completed"
JOB_STATUS_TERMINATING = "Terminating"
JOB_STATUS_TERMINATED = "Terminated"
JOB_STATUS_FAILED = "Failed"
JOB_STATUS_RESTARTING = "Restarting"
JOB_STATUS_ABORTED = "Aborted"
JOB_STATUS_ABORTING = "Aborting"
JOB_STATUS_RUNNING = "Running"

COMMON = "https://grafana.digitalbrain.cn:32443/d-solo/3JLLppA4k/notebookjian-kong?"
LOG_COMMON = "https://grafana.digitalbrain.cn:32443/d/o6-BGgnnk/kubernetes-logs?"


class Job(GenericDateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_job"
        metadata = META
        database = DB
        orders_by = ['-id']

    name: str = ormar.String(max_length=20, comment='名称')
    storage: str = ormar.JSON(comment='存储信息')
    mode: str = ormar.String(max_length=40)
    start_command: str = ormar.Text(comment='启动命令')

    custom: bool = ormar.Boolean(default=False)
    image: str = ormar.String(max_length=150, comment='镜像名称')

    status: Status = ormar.ForeignKey(Status, related_name='job_status')
    start_mode: Mode = ormar.ForeignKey(Mode, related_name='job_start_mode')
    nodes: int = ormar.Integer(comment='任务节点数量')
    work_dir: str = ormar.String(max_length=100, comment='工作目录', nullable=True)
    k8s_info: dict = ormar.JSON(comment="集群信息")

    cpu: int = ormar.Integer(comment='CPU数量')
    memory: int = ormar.Integer(comment='存储容量G')
    gpu: int = ormar.Integer(comment='GPU数量')
    type: str = ormar.String(max_length=40, default='', comment='CPU/GPU类型')
    url: str = ormar.String(max_length=160, comment='url地址', nullable=True)
    server_ip: str = ormar.String(max_length=20, comment='所在的node', nullable=True)


    @classmethod
    async def all_jobs(cls):
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
    async def get_job_related_status_by_pk(cls, pk):
        return await Job.objects.select_related(['status']).get(pk=pk)

    @property
    def namespace_name(self):
        return f"{self.k8s_info.get('namespace')}"

    @property
    def pod_name(self):
        return f"{self.k8s_info.get('name')}-tfjob-0"

    @property
    def start_time_timestamp(self):
        return int(time.mktime(self.started_at.utctimetuple())) if self.started_at \
            else int(time.mktime(datetime.datetime.utcnow().utctimetuple()))


    @property
    def ended_time_timestamp(self):
        return int(time.mktime(self.ended_at.utctimetuple())) if self.ended_at \
            else int(time.mktime(datetime.datetime.utcnow().utctimetuple()))

    @property
    def cpu_url(self):
        return f"{COMMON}orgId=1&var-namespace={self.namespace_name}&var-cluster=&var-job={self.pod_name}&panelId=4&from={self.start_time_timestamp}&to={self.ended_time_timestamp}"

    @property
    def gpu_url(self):
        if self.gpu > 0:
            return f"{COMMON}orgId=1&var-namespace={self.namespace_name}&var-cluster=&var-job={self.pod_name}&panelId=8&from={self.start_time_timestamp}&to={self.ended_time_timestamp}"
        else:
            return ""

    @property
    def ram_url(self):
        return f"{COMMON}orgId=1&var-namespace={self.namespace_name}&var-cluster=&var-job={self.pod_name}&panelId=6&from={self.start_time_timestamp}&to={self.ended_time_timestamp}"

    @property
    def vram_url(self):
        if self.gpu > 0:
            return f"{COMMON}orgId=1&var-namespace={self.namespace_name}&var-cluster=&var-job={self.pod_name}&panelId=12&from={self.start_time_timestamp}&to={self.ended_time_timestamp}"
        else:
            return ""


    @property
    def logging_url(self):
        return f"{LOG_COMMON}orgId=1&theme=light&viewPanel=2&var-namespace={self.namespace_name}&var-app={self.create_en_by}-{self.name}"


    @property
    def source(self):
        if self.gpu:
            return f"GPU {self.gpu}*{self.type} {self.cpu}C {self.memory}G"
        else:
            return f"CPU {self.cpu}C {self.memory}G"


    @property
    def webkubectl(self):
        return f"{WEBKUBECTL_URL}/?arg=-n{self.project_en_by}&arg={self.create_en_by}-{self.name}-tfjob-0&arg=bash"

    def gen_job_pagation_response(self):
        return {
            "id": self.id,
            "status": {"code": self.status.code,
                       "name": self.status.name,
                       "desc": self.status.desc,},
            "name": self.name,
            "source": self.source,
            "creator": {"id": self.created_by_id,
                        "username": self.created_by,},
            "project": {"id": self.project_by_id,
                        "name": self.project_by,},
            "image": {"name": self.image,
                      "custom": self.custom,},
            "url": self.webkubectl,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "mode": self.mode,
        }

    def gen_job_simple_response(self):
        return {
            "id": self.id,
            "status": self.status.name,
            "name": self.name,
            "creator": {"id": self.created_by_id,
                        "username": self.created_by,},
            "project": {"id": self.project_by_id,
                        "name": self.project_by,},
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "mode": self.mode,
            "volume_ids": [x['storage']['id'] for x in self.storage],
        }

    def gen_job_detail_response(self):
        return {
            "id": self.id,
            "status": {"code": self.status.code,
                       "name": self.status.name,
                       "desc": self.status.desc, },
            "name": self.name,
            "creator": {"id": self.created_by_id,
                        "username": self.created_by,},
            "project": {"id": self.project_by_id,
                        "name": self.project_by,},
            "image": {"name": self.image,
                      "custom": self.custom,},
            "source": self.source,
            "mode": self.mode,
            "start_command": self.start_command,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
            "hooks": self.storage,
            "grafana": {"cpu": self.cpu_url,
                        "gpu": self.gpu_url,
                        "ram": self.ram_url,
                        "vram": self.vram_url,},
            "url": self.webkubectl,
            "logging_url": self.logging_url,
            "work_dir": self.work_dir,
            "start_mode": {
                "id": self.start_mode.id,
                "name": self.start_mode.name,
            },
            "nodes": self.nodes,
        }

    @classmethod
    def compare_status_and_update(cls, status: str, status_dic):
        if status == JOB_STATUS_PENDING:
            return status_dic['pending']
        elif status == JOB_STATUS_RUNNING:
            return status_dic['run']
        elif status == JOB_STATUS_FAILED:
            return status_dic['run_fail']
        elif status in {JOB_STATUS_COMPLETED, JOB_STATUS_COMPLETING}:
            return status_dic['completed']
        elif status in {JOB_STATUS_TERMINATING, JOB_STATUS_TERMINATED, JOB_STATUS_ABORTED, JOB_STATUS_ABORTING}:
            return status_dic['error']
        return 1

    @classmethod
    async def project_list_by_ip(cls, _ip: str):
        return await cls.objects.all(cls.server_ip == _ip, status__in=[4, 11])
