"""
启动入口、根路由配置
"""
import os
import uvicorn
from fastapi import FastAPI
from namespace.api import router_namespace
from pvc.api import router_pvc
from notebook.api import router_notebook
from starlette.middleware.base import BaseHTTPMiddleware
from basic.middleware.exception import validation_pydantic_exception_handler
from basic.middleware.rsp import add_common_response_data
from pydantic.error_wrappers import ValidationError

app = FastAPI()


@app.get('/status')
def status():
    return {"status": "ok"}

app.include_router(router_namespace, prefix="/namespace")
app.include_router(router_pvc, prefix="/pvc")
app.include_router(router_notebook, prefix="/notebook")


app.add_middleware(BaseHTTPMiddleware, dispatch=add_common_response_data)

# 异常处理
app.add_exception_handler(ValidationError, validation_pydantic_exception_handler)

def start():
    service_port = int(os.getenv('CLUSTER_SERVICE_PORT', 80))
    uvicorn.run(
        'main:app', host="0.0.0.0", port=service_port,
        reload=False,
        # debug=DEBUG,
        workers=2
    )

# USER_SERVICE_PORT
if __name__ == '__main__':
    start()
