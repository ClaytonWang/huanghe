# -*- coding: utf-8 -*-
"""
    >File    : base_model.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/10 20:01
"""
import ormar

from datetime import datetime
from sqlalchemy import func



"""
Mixin
eg:
    class Category(ormar.Model, DateFieldsMixins, AuditMixin):
        class Meta(ormar.ModelMeta):
            tablename = "categories"
            metadata = metadata
            database = db
    
        id: int = ormar.Integer(primary_key=True)
        name: str = ormar.String(max_length=50, unique=True, index=True)
"""


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class AuditMixin:
    created_by: str = ormar.Integer(comment='创建者', nullable=True)
    updated_by: str = ormar.Integer(comment='更新者', nullable=True)


class DateFieldsMixins:
    created_at: datetime = ormar.DateTime(default=datetime.now)
    updated_at: datetime = ormar.DateTime(default=datetime.now)


"""
Inherit

eg:
    class Category(DateFieldsModel, AuditModel):
        class Meta(ormar.ModelMeta):
            tablename = "categories"
    
        id: int = ormar.Integer(primary_key=True)
        name: str = ormar.String(max_length=50, unique=True, index=True)
"""


class AuditModel(ormar.Model):
    class Meta:
        alias_generator = to_camel
        abstract = True

    created_by: str = ormar.Integer(comment='创建者', nullable=True)
    updated_by: str = ormar.Integer(comment='更新者', nullable=True)


class DateModel(ormar.Model):
    class Meta:
        alias_generator = to_camel
        abstract = True

    created_at: datetime = ormar.DateTime(default=datetime.now)
    updated_at: datetime = ormar.DateTime(default=datetime.now)


class DateAuditModel(ormar.Model):
    class Meta:
        alias_generator = to_camel
        abstract = True

    id: int = ormar.Integer(primary_key=True)
    created_by: int = ormar.Integer(comment='创建者', nullable=True)
    updated_by: int = ormar.Integer(comment='更新者', nullable=True)

    created_at: datetime = ormar.DateTime(server_default=func.now(), comment='创建日期')
    updated_at: datetime = ormar.DateTime(server_default=func.now(), onupdate=func.now(), comment='更新日期')



class GenericDateModel(ormar.Model):
    class Meta:
        alias_generator = to_camel
        abstract = True

    id: int = ormar.Integer(primary_key=True)
    created_by_id: int = ormar.Integer(comment='创建者id', nullable=True)
    updated_by_id: int = ormar.Integer(comment='更新者id', nullable=True)
    project_by_id: int = ormar.Integer(comment='创建项目id', nullable=True)

    created_by: str = ormar.String(max_length=12, nullable=True, comment="创建者")
    updated_by: str = ormar.String(max_length=12, nullable=True, comment="更新者")
    project_by: str = ormar.String(max_length=12, nullable=True, comment="创建项目")

    create_en_by: str = ormar.String(max_length=20, nullable=True, comment="创建者英文名")
    project_en_by: str = ormar.String(max_length=20, nullable=True, comment="创建项目英文名")

    created_at: datetime = ormar.DateTime(server_default=func.now(), comment='创建日期')
    updated_at: datetime = ormar.DateTime(server_default=func.now(), onupdate=func.now(), comment='更新日期')
    deleted_at: datetime = ormar.DateTime(comment="删除日期", nullable=True)
    started_at: datetime = ormar.DateTime(comment="启动日期")
    ended_at: datetime = ormar.DateTime(comment="结束日期")

class GenericNoProjectModel(ormar.Model):
    class Meta:
        alias_generator = to_camel
        abstract = True

    id: int = ormar.Integer(primary_key=True)
    created_by_id: int = ormar.Integer(comment='创建者id', nullable=True)
    updated_by_id: int = ormar.Integer(comment='更新者id', nullable=True)

    created_by: str = ormar.String(max_length=12, nullable=True, comment="创建者")
    updated_by: str = ormar.String(max_length=12, nullable=True, comment="更新者")

    create_en_by: str = ormar.String(max_length=20, nullable=True, comment="创建者英文名")

    created_at: datetime = ormar.DateTime(server_default=func.now(), comment='创建日期')
    updated_at: datetime = ormar.DateTime(server_default=func.now(), onupdate=func.now(), comment='更新日期')
    deleted_at: datetime = ormar.DateTime(comment="删除日期", nullable=True)

class OnlyPrimaryKeyModel(ormar.Model):
    class Meta:
        alias_generator = to_camel
        abstract = True

    id: int = ormar.Integer(primary_key=True)
