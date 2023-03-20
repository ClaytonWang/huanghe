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
from basic.config.job_management import WEBKUBECTL_URL
from basic.common.base_model import GenericDateModel
from basic.common.status_cache import Status
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


class Deployment(GenericDateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_deployment"
        metadata = META
        database = DB
        orders_by = ['-id']

    name: str = ormar.String(max_length=20, comment='名称')
    storage: str = ormar.JSON(comment='存储信息')
    private_ip: str = ormar.String(max_length=20, comment='私网IP')
    public_ip: str = ormar.String(max_length=20, comment='公网IP')
    port: int = ormar.Integer(comment='端口')

    custom: bool = ormar.Boolean(default=False)
    image: str = ormar.String(max_length=150, comment='镜像名称')

    status: Status = ormar.ForeignKey(Status, related_name='deployment_status')
    work_dir: str = ormar.String(max_length=100, comment='工作目录', nullable=True)
    k8s_info: dict = ormar.JSON(comment="集群信息")

    cpu: int = ormar.Integer(comment='CPU数量')
    memory: int = ormar.Integer(comment='存储容量G')
    gpu: int = ormar.Integer(comment='GPU数量')
    type: str = ormar.String(max_length=40, default='', comment='CPU/GPU类型')
    url: str = ormar.String(max_length=160, comment='url地址', nullable=True)
    server_ip: str = ormar.String(max_length=20, comment='所在的node', nullable=True)

    @classmethod
    async def all_deployments(cls):
        return cls.objects.filter()
