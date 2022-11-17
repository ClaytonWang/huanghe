from contextlib import contextmanager

import psycopg2.extras
import psycopg2.pool
from sqlalchemy import create_engine

POSTGRES_URI_PATTERN = 'postgresql://{user}:{password}@{host_name}:{port}/{database}'
DATABASE_NAME = "DATABASE_NAME"
DATABASE_USERNAME = "DATABASE_USERNAME"
DATABASE_PASSWORD = "DATABASE_PASSWORD"


# Postgresql 数据大量读写的Pool对象
POOL = psycopg2.pool.SimpleConnectionPool(
    minconn=10,
    maxconn=20,
    host="localhost",
    port=5432,
    database=DATABASE_NAME,
    user=DATABASE_USERNAME,
    password=DATABASE_PASSWORD
)


@contextmanager
def get_conn():
    conn = POOL.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        POOL.putconn(conn)


@contextmanager
def get_cursor():
    with get_conn() as conn:
        yield conn.cursor()


@contextmanager
def get_dict_cursor():
    with get_conn() as conn:
        yield conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def get_pg_engine(db_name):
    pg_engine = POSTGRES_URI_PATTERN.format(user=DATABASE_USERNAME,
                                            password=DATABASE_PASSWORD,
                                            host_name="localhost",
                                            port=5432,
                                            database=db_name)
    engine = create_engine(pg_engine)
    return engine
