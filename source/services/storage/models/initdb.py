# -*- coding: utf-8 -*-
"""
    >File    : initdb.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/24 09:45
"""
import databases
import sqlalchemy
from config import DATABASES

DB_CONN = f'{DATABASES["USER"]}:{DATABASES["PASSWORD"]}@{DATABASES["HOST"]}:{DATABASES["PORT"]}/{DATABASES["NAME"]}'

DB_POSTGRESQL_CONN = f'postgresql://{DB_CONN}'

DB = databases.Database(DB_POSTGRESQL_CONN)
META = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DB_POSTGRESQL_CONN)
META.create_all(engine)


async def startup_event() -> None:
    if not DB.is_connected:
        await DB.connect()


async def shutdown_event() -> None:
    if DB.is_connected:
        await DB.disconnect()
