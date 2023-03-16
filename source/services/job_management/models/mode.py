from basic.common.base_model import DateModel
from basic.common.initdb import DB, META
import ormar


cache_pagation = []
cache_mapping = {}
class Mode(DateModel):
    """
    mvp3
    多机多卡模块
    任务详情页-启动方式
    """
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_mode"
        metadata = META
        database = DB
        orders_by = ['id']

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=40, default='', comment="启动模式名称")
    desc: str = ormar.String(max_length=80, default='', comment='备注')
    max_nodes: int = ormar.Integer(default=1, comment="限制节点数量")

    def gen_pagation(self):
        return {
            "id": self.id,
            "max_nodes": self.max_nodes,
            "name": self.name,
        }

    @classmethod
    async def all(cls):
        return await Mode.objects.all()

    @classmethod
    async def mode_cache_pagation(cls) -> list[dict]:
        global cache_pagation
        if not cache_pagation:
            cache_pagation = [mode.gen_pagation() for mode in await cls.all()]
        return cache_pagation

    @classmethod
    async def get(cls, key):
        global cache_mapping
        if not cache_mapping:
            cache_mapping = {}
            for mode in await cls.mode_cache_pagation():
                cache_mapping[mode["id"]] = mode["name"]
        return cache_mapping[key]



