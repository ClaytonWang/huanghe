"""
启动入口、根路由配置
"""
import os
import uvicorn
from fastapi import FastAPI
from volume.api import router_volume
from models import startup_event, shutdown_event
from basic.middleware.account_getter import verify_token
from starlette.middleware.base import BaseHTTPMiddleware
from basic.middleware.exception import validation_pydantic_exception_handler
from basic.middleware.exception import validation_ormar_exception_handler
from basic.middleware.exception import ormar_db_exception_handler
from asyncpg.exceptions import PostgresError
from pydantic.error_wrappers import ValidationError
from config import *
from fastapi.exceptions import RequestValidationError
from basic.middleware.rsp import add_common_response_data

app = FastAPI()


@app.get('/status')
def status():
    return {"status": "ok"}


app.include_router(router_volume, prefix="/volume")

# 配置中间件
app.add_middleware(BaseHTTPMiddleware, dispatch=verify_token)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_common_response_data)

# 异常处理
app.add_exception_handler(ValidationError, validation_pydantic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_ormar_exception_handler)
app.add_exception_handler(PostgresError, ormar_db_exception_handler)

# 配置数据库连接
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


def start():
    service_port = int(os.getenv('STORAGE_SERVICE_PORT', 8003))
    uvicorn.run(
        'main:app', port=service_port,
        reload=False,
        # debug=DEBUG,
        workers=2,

    )


# USER_SERVICE_PORT
if __name__ == '__main__':
    start()
