import ormar
from basic.common.base_model import DateModel, OnlyPrimaryKeyModel
from servers.serializers import ServerCreateReq
from initdb import DB, META
from basic.middleware.rsp import success_common_response
from notebook_management.models.notebook import Notebook


class Server(OnlyPrimaryKeyModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_servers"
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
    def gen_create_dict(self, scr: ServerCreateReq):
        return {
            "cpu": scr.cpu,
            "memory": scr.memory,
            "gpu": scr.gpu,
            "type": scr.type,
            "status": scr.status,
            "server": scr.server,
        }

    @classmethod
    def gen_server_pagation_response(self, scr: ServerCreateReq):
        return {
            "id": scr.id,
            "status": scr.status,
            "server": scr.server,
            "occupied_rate": "1/3",
            "source": self.get_str(scr),
            "occupied_by": [{"id": 1, "username": "张三"},
                            {"id": 2, "username": "李四"}]
        }

    @classmethod
    async def create_node_database(self, scr: ServerCreateReq):
        node = await Server.objects.get_or_none(server=scr.server)
        if node is None:
            await Server.objects.create(**Server.gen_create_dict(scr))
        else:
            await Server.objects.filter(server=scr.server).update(status=scr.status)
        return success_common_response()


    @classmethod
    async def all_servers(cls):
        return cls.objects.filter()

# filterif __name__ == '__main__':
#
#     server= Server().get_server_occupied()
