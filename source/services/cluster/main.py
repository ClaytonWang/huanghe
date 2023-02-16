"""
启动入口、根路由配置
"""
import os
import uvicorn
from fastapi import FastAPI, status as st
from fastapi.responses import JSONResponse
from namespace.api import router_namespace
from pod.api import router_pod
from pvc.api import router_pvc
from notebook.api import router_notebook
from secret.api import router_secret
from volcanojob.api import router_vcjob
from server.api import router_server
from starlette.middleware.base import BaseHTTPMiddleware
from basic.middleware.exception import validation_pydantic_exception_handler
from basic.middleware.rsp import add_common_response_data
from pydantic.error_wrappers import ValidationError
from kubernetes.client import ApiException

app = FastAPI()


def k8s_exception_handler(request, exc):
    if isinstance(exc, (ApiException, )):
        return JSONResponse(eval(exc.body).get("reason"), status_code=st.HTTP_400_BAD_REQUEST)

    return exc

@app.get('/status')
def status():
    return {"status": "ok"}

app.include_router(router_namespace, prefix="/namespace")
app.include_router(router_pvc, prefix="/pvc")
app.include_router(router_notebook, prefix="/notebook")
app.include_router(router_secret, prefix='/secret')
app.include_router(router_vcjob, prefix='/job')
app.include_router(router_server, prefix='/server')
app.include_router(router_pod, prefix='/pod')

app.add_middleware(BaseHTTPMiddleware, dispatch=add_common_response_data)

# 异常处理
app.add_exception_handler(ValidationError, validation_pydantic_exception_handler)
app.add_exception_handler(ApiException, k8s_exception_handler)


def start():
    service_port = int(os.getenv('CLUSTER_SERVICE_PORT', 80))
    uvicorn.run(
        'main:app', host="0.0.0.0", port=service_port,
        reload=True,
        # debug=DEBUG,
        workers=2
    )

# USER_SERVICE_PORT
if __name__ == '__main__':
    start()
