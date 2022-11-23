# -*- coding: utf-8 -*-
"""
    >File    : base_model.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/10 20:01
"""
import ormar
import databases
import sqlalchemy
from datetime import datetime
from config import DATABASES
from sqlalchemy import func

DB_CONN = f'{DATABASES["USER"]}:{DATABASES["PASSWORD"]}@{DATABASES["HOST"]}:{DATABASES["PORT"]}/{DATABASES["NAME"]}'
DB_POSTGRESQL_CONN = f'postgresql://{DB_CONN}'


DATABASE = databases.Database(DB_POSTGRESQL_CONN)
METADATA = sqlalchemy.MetaData()



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
    created_by: str = ormar.String(max_length=100)
    updated_by: str = ormar.String(max_length=100, default="Sam")


class DateFieldsMixins:
    created_date: datetime = ormar.DateTime(default=datetime.now)
    updated_date: datetime = ormar.DateTime(default=datetime.now)


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
        metadata = METADATA
        database = DATABASE

    created_by: str = ormar.String(max_length=100)
    updated_by: str = ormar.String(max_length=100, default="Sam")


class DateModel(ormar.Model):
    class Meta:
        alias_generator = to_camel
        abstract = True
        metadata = METADATA
        database = DATABASE

    created_date: datetime = ormar.DateTime(default=datetime.now)
    updated_date: datetime = ormar.DateTime(default=datetime.now)


class DateAuditModel(ormar.Model):
    class Meta:
        alias_generator = to_camel
        abstract = True
        metadata = METADATA
        database = DATABASE

    created_by: str = ormar.Integer(comment='创建者', nullable=True)
    updated_by: str = ormar.Integer(comment='更新者', nullable=True)

    created_date: datetime = ormar.DateTime(server_default=func.now(), comment='创建日期')
    updated_date: datetime = ormar.DateTime(server_default=func.now(), onupdate=func.now(), comment='更新日期')
