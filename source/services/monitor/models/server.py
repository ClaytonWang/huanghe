import ormar
from basic.common.base_model import OnlyPrimaryKeyModel
from services.monitor.servers.serializers import ServerCreateReq
from basic.common.initdb import DB, META
from basic.middleware.rsp import success_common_response


class Server(OnlyPrimaryKeyModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_servers"
        metadata = META
        database = DB
        orders_by = ['-id']
    server_ip: str = ormar.String(max_length=18, comment='服务器IP地址', nullable=True)
    server: str = ormar.String(max_length=18, comment='服务器名称')
    status: str = ormar.String(max_length=17, comment='服务器状态')
    cpu: int = ormar.Integer(comment='CPU总数')
    memory: int = ormar.Integer(comment='存储容量G')
    gpu: int = ormar.Integer(comment='GPU数量')
    type: str = ormar.String(max_length=40, default='', comnet='CPU/GPU类型')
    occupied_cpu: int = ormar.Integer(comment='被占用CPU总数', nullable=True)
    occupied_gpu: int = ormar.Integer(comment='被占用GPU总数', nullable=True)
    occupied_memory: int = ormar.Integer(comment='被占用内存总数', nullable=True)
    occupied_by: str = ormar.JSON(comment='占用人', nullable=True)

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
            "server_ip": scr.server_ip
        }

    @classmethod
    def gen_server_pagation_response(cls, scr: ServerCreateReq):
        return {
            "id": scr.id,
            "status": scr.status,
            "server": scr.server_ip,
            "occupied_rate": cls.get_occupied_rate(scr),
            "source": cls.get_str(scr),
            "occupied_by": scr.occupied_by
        }

    def get_occupied_rate(self):
        res = max(self.occupied_cpu / self.cpu, self.occupied_memory / self.memory)
        if (self.type != "cpu" and (self.occupied_gpu / self.gpu) <= res) or (self.type == "cpu"):
            if self.occupied_cpu / self.cpu >= self.occupied_memory / self.memory:
                if self.occupied_cpu == 0:
                    return "0"
                else:
                    return f"{self.occupied_cpu}/{self.cpu}"
            else:
                if self.occupied_memory == 0:
                    return "0"
                else:
                    return f"{self.occupied_memory}/{self.memory}"
        else:
            return f"{self.occupied_gpu}/{self.gpu}"

    @classmethod
    async def create_node_database(self, scr: ServerCreateReq):
        node = await Server.objects.get_or_none(server=scr.server)
        if node is None:
            await Server.objects.create(**Server.gen_create_dict(scr))
        else:
            await Server.objects.filter(server=scr.server).update(status=scr.status, occupied_cpu=scr.occupied_cpu,
                                                                  occupied_gpu=scr.occupied_gpu,
                                                                  occupied_memory=scr.occupied_memory,
                                                                  occupied_by=scr.occupied_by,server_ip=scr.server_ip)
        return success_common_response()


    @classmethod
    async def all_servers(cls):
        return cls.objects.filter()
