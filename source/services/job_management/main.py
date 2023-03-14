"""
启动入口、根路由配置
"""

import uvicorn
from asyncpg.exceptions import PostgresError
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from ormar.exceptions import AsyncOrmException
from pydantic.error_wrappers import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from basic.common.env_variable import get_integer_variable
from basic.common.env_variable import get_string_variable
from config import *
from basic.middleware.auth import OFOAuth2PasswordBearer
from basic.middleware.exception import ormar_db_exception_handler
from basic.middleware.exception import pg_db_exception_handler
from basic.middleware.exception import validation_ormar_exception_handler
from basic.middleware.exception import validation_pydantic_exception_handler
from basic.middleware.rsp import add_common_response_data
from basic.utils.log import configure_logging
from basic.common.initdb import startup_event, shutdown_event
from job.api import router_job
from basic.middleware.account_getter import verify_token
from basic.middleware.service_requests import get_source_list, get_image_list


configure_logging('logging.config.dictConfig', LOGGING)
app = FastAPI(
    title='job管理',
    tags=["FastAPI job管理模块"],
    # dependencies=[Depends(oauth2_scheme)]
)

# 配置中间件
app.add_middleware(BaseHTTPMiddleware, dispatch=verify_token)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_common_response_data)

# 配置数据库连接
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


app.add_exception_handler(ValidationError, validation_pydantic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_ormar_exception_handler)
app.add_exception_handler(PostgresError, pg_db_exception_handler)
app.add_exception_handler(AsyncOrmException, ormar_db_exception_handler)


@app.get('/status')
def status():
    return {"status": "ok"}


@app.get('/image')
async def get_image(request: Request):
    authorization: str = request.headers.get('authorization')
    res_image = await get_image_list(authorization)
    return res_image


@app.get('/source')
async def get_source(request: Request):
    authorization: str = request.headers.get('authorization')
    res_source = await get_source_list(authorization)
    return res_source


# 路由配置
app.include_router(router_job, prefix='/jobs', tags=['job'])


if __name__ == '__main__':
    from multiprocessing import cpu_count
    print("cpu_count: ", cpu_count())
    service_port = get_integer_variable('JOB_SERVICE_PORT', SERVICE_PORT)
    debug = False if 'PRODUCTION' == get_string_variable('ENV', 'DEV') else True

    # -workers INTEGER
    # Number of worker processes. Defaults to the $WEB_CONCURRENCY environment variable if available, or 1.
    # Not valid with --reload.
    uvicorn.run(
        'main:app', host='0.0.0.0', port=service_port,
        reload=True,
        debug=debug,
        workers=2
    )
