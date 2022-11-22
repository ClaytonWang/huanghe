"""
启动入口、根路由配置
"""
import os
import uvicorn
from fastapi import FastAPI, Depends
# from apps.users.views import router_user
# from apps.auth.views import router_auth
# from fastapi.security import OAuth2PasswordBearer
# from starlette.middleware.base import BaseHTTPMiddleware
# from settings import DEBUG, LOGGING
# from utils.log import configure_logging
# from utils.middleware import verify_token
# import os

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# configure_logging('logging.config.dictConfig', LOGGING)
app = FastAPI(
    tags=["FastAPI 登录&验证"],
    # dependencies=[Depends(oauth2_scheme)]
)
# # app.add_middleware(BaseHTTPMiddleware, dispatch=verify_token)

# 路由配置
# app.include_router(router_auth, prefix='/auth')


@app.get('/v1/hello')
def hello():
    return "hello world"


service_port = int(os.getenv('USER_SERVICE_PORT', 0))
if not service_port:
    service_port = 8000

# USER_SERVICE_PORT
if __name__ == '__main__':
    uvicorn.run(
        'main:app', host='0.0.0.0', port=service_port,
        reload=False,
        # debug=DEBUG,
        workers=2
    )
