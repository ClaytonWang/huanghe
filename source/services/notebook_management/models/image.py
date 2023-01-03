# -*- coding: utf-8 -*-
"""
    >File   : image.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/21 17:32
"""

import ormar
from basic.common.base_model import DateModel
from models import DB, META


# todo 镜像放在notebook里做临时方案,先用主键关联凑合下后期看是否分离单独配置,不用外键了怕麻烦
class Image(DateModel):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_image"
        metadata = META
        database = DB
        orders_by = ['-id']

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=40, comnet='镜像名称', unique=True)
    desc: str = ormar.String(max_length=80, default='', comnet='镜像描述')

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
        }


