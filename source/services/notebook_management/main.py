"""
启动入口、根路由配置
"""

import uvicorn
from config import *
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from asyncpg.exceptions import PostgresError
from pydantic.error_wrappers import ValidationError
from fastapi.exceptions import RequestValidationError
from basic.utils.log import configure_logging
from basic.middleware.rsp import add_common_response_data
from basic.middleware.auth import OFOAuth2PasswordBearer
from basic.common.env_variable import get_integer_variable
from basic.common.env_variable import get_string_variable
from basic.middleware.exception import validation_pydantic_exception_handler
from basic.middleware.exception import validation_ormar_exception_handler
from basic.middleware.exception import ormar_db_exception_handler
from basic.middleware.exception import pg_db_exception_handler
from ormar.exceptions import AsyncOrmException
from utils.auth import verify_token
from notebook.api import router_notebook
from models import startup_event, shutdown_event


# oauth2_scheme = OFOAuth2PasswordBearer(token_url="/v1/auth/login")
oauth2_scheme = OFOAuth2PasswordBearer(token_url=USER_SERVICE_PATH + "/v1/auth/login")
configure_logging('logging.config.dictConfig', LOGGING)
app = FastAPI(
    title='notebook管理',
    tags=["FastAPI notebook管理模块"],
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

# 路由配置
app.include_router(router_notebook, prefix='/notebooks', tags=['Notebook'])


if __name__ == '__main__':
    from multiprocessing import cpu_count
    print("cpu_count: ", cpu_count())
    service_port = get_integer_variable('NOTEBOOK_SERVICE_PORT', SERVICE_PORT)
    debug = False if 'PRODUCTION' == get_string_variable('ENV', 'DEV') else DEBUG

    # todo 把轮询k8s的scheduler放在一起启动

    # -workers INTEGER
    # Number of worker processes. Defaults to the $WEB_CONCURRENCY environment variable if available, or 1.
    # Not valid with --reload.
    uvicorn.run(
        'main:app', host='0.0.0.0', port=service_port,
        reload=False if debug else True,
        debug=debug,
        workers=2
    )
