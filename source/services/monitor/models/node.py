import ormar
from basic.common.base_model import DateModel, OnlyPrimaryKeyModel
from source.services.monitor.node.serializers import NodeCreate
from .initdb import DB, META


class Node(OnlyPrimaryKeyModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_node"
        metadata = META
        database = DB
        orders_by = ['-id']

    server: str = ormar.String(max_length=18, comment='服务器IP地址')
    status: str = ormar.String(max_length=17, comment='服务器状态')
    cpu: int = ormar.Integer(comment='CPU总数')
    memory: int = ormar.Integer(comment='存储容量G')
    gpu: int = ormar.Integer(comment='GPU数量')
    type: str = ormar.String(max_length=40, default='', comnet='CPU/GPU类型')

    def get_str(self):
        if self.gpu:
            return f"GPU {self.gpu}*{self.type} {self.cpu}C {self.memory}G"
        else:
            return f"CPU {self.cpu}C {self.memory}G"

    @classmethod
    def gen_create_dict(self, ncr: NodeCreate):
        return {
            "cpu": ncr.cpu,
            "memory": ncr.memory,
            "gpu": ncr.gpu,
            "type": ncr.type,
            "status": ncr.status,
            "server": ncr.server,
        }

    @classmethod
    def gen_node_pagation_response(self, ncr: NodeCreate):
        return {
            "id": ncr.id,
            "status": ncr.status,
            "server": ncr.server,
            "occupied_rate": "1/3",
            "source": self.get_str(ncr),
            "occupied_by": [{"id": 1, "username": "张三"},
                            {"id": 2, "username": "李四"}]
        }

    @classmethod
    async def undeleted_nodes(cls):
        return cls.objects.filter()
