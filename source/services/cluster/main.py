"""
启动入口、根路由配置
"""
import os
import uvicorn
from fastapi import FastAPI

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# configure_logging('logging.config.dictConfig', LOGGING)
app = FastAPI()
# # app.add_middleware(BaseHTTPMiddleware, dispatch=verify_token)

# 路由配置
# app.include_router(router_auth, prefix='/auth')


@app.get('/status')
def status():
    return {"status": "ok"}


service_port = os.getenv('USER_SERVICE_PORT', "").upper()
if not service_port:
    service_port = 80

# USER_SERVICE_PORT
if __name__ == '__main__':
    uvicorn.run(
        'main:app',  port=service_port,
        reload=False,
        # debug=DEBUG,
        workers=2
    )
