"""
启动入口、根路由配置
"""

import uvicorn
from fastapi import FastAPI, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from config import *
from basic.utils.log import configure_logging
from basic.middleware.auth import verify_token
from basic.middleware.rsp import add_common_response_data
from basic.middleware.auth import OFOAuth2PasswordBearer
from api.auth_api import router_auth
from api.user_api import router_user

oauth2_scheme = OFOAuth2PasswordBearer(token_url="/v1/auth/login")
configure_logging('logging.config.dictConfig', LOGGING)
app = FastAPI(
    tags=["FastAPI 用户验证模块"],
    dependencies=[Depends(oauth2_scheme)]
)
app.add_middleware(BaseHTTPMiddleware, dispatch=verify_token)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_common_response_data)


@app.on_event("startup")
async def startup() -> None:
    from models.base_model import DATABASE
    if not DATABASE.is_connected:
        await DATABASE.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    from models.base_model import DATABASE
    # database_ = app.state.database
    if DATABASE.is_connected:
        await DATABASE.disconnect()


# 路由配置
app.include_router(router_auth, prefix='/v1/auth')
app.include_router(router_user, prefix='/v1/users')


if __name__ == '__main__':
    service_port = int(os.getenv('USER_SERVICE_PORT', 0))
    if not service_port:
        service_port = SERVICE_PORT

    env = os.getenv('ENV', '').upper()
    if env == 'PROD':
        debug = False
    else:
        debug = DEBUG

    uvicorn.run(
        'main:app', host='0.0.0.0', port=service_port,
        reload=False if debug else True,
        debug=debug,
        workers=2
    )
