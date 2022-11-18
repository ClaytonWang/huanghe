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
from settings import DATABASES


DB_CONN = f'{DATABASES["USER"]}:{DATABASES["PASSWORD"]}@{DATABASES["HOST"]}:{DATABASES["PORT"]}/{DATABASES["NAME"]}'
DB_POSTGRESQL_CONN = f'postgres://{DB_CONN}'
DB_MYSQL_CONN = f'mysql://{DB_CONN}'
DB_SQLITE_CONN = "sqlite:///db.sqlite"

DATABASE = databases.Database(DB_SQLITE_CONN)
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


class DateFieldsModel(ormar.Model):
    class Meta:
        alias_generator = to_camel
        abstract = True
        metadata = METADATA
        database = DATABASE

    created_date: datetime = ormar.DateTime(default=datetime.now)
    updated_date: datetime = ormar.DateTime(default=datetime.now)
