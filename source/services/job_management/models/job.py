# -*- coding: utf-8 -*-
"""
    >File   : job.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/14 18:58
"""

from __future__ import annotations

import ormar

from basic.common.base_model import DateModel, GenericDateModel
from models import DB, META


# 状态
# JOB_STATUS_PENDING = "pending"  # 排队中     3
# JOB_STATUS_RUNNING = "running"  # 已启动(运行中)    4
# JOB_STATUS_STOP = "stop"  # 停止中       2
# JOB_STATUS_START_FAIL = "start_fail"  # 启动失败  7
# JOB_STATUS_RUN_FAIL = "run_fail"  # 运行失败  8
# JOB_STATUS_STOP_FAIL = "stop_fail"  # 停止失败    9
# JOB_STATUS_COMPLETED = "completed"  # 已完成       10
# JOB_STATUS_STOPPED = "stopped"  # 已停止 5


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


class Job(GenericDateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_job"
        metadata = META
        database = DB
        orders_by = ['-id']

    name: str = ormar.String(max_length=20, comnet='名称')
    storage: str = ormar.JSON(comment='存储信息')
    task_model: int = ormar.Integer(default=0, comment='任务模式，0：调试，1：非调试')
    start_command: str = ormar.Text(comment='启动命令')
    image_type: int = ormar.Integer(default=0, comment='镜像类型，0：官方镜像，1：自定义镜像')
    image_name: str = ormar.String(max_length=100, comment='镜像名称')
    status: Status = ormar.ForeignKey(Status, related_name='job_status')
    work_dir: str = ormar.String(max_length=100, comment='工作目录')
    source_id: int = ormar.Integer(comment='source表id逻辑关联')
    k8s_info:str = ormar.JSON(comment="集群信息")

    def get_task_model_name(self):
        if self.task_model == 0:
            return "调试"
        if self.task_model == 1:
            return "非调试"
        return self.task_model

