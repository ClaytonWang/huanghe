"""
启动入口、根路由配置
"""
import os
import uvicorn
from fastapi import FastAPI
from namespace.api import router_namespace
from pvc.api import router_pvc
from notebook.api import router_notebook

app = FastAPI()


@app.get('/status')
def status():
    return {"status": "ok"}

app.include_router(router_namespace, prefix="/namespace")
app.include_router(router_pvc, prefix="/pvc")
app.include_router(router_notebook, prefix="/notebook")

def start():
    service_port = int(os.getenv('CLUSTER_SERVICE_PORT', 8005))
    uvicorn.run(
        'main:app', port=service_port,
        reload=False,
        # debug=DEBUG,
        workers=2
    )

# USER_SERVICE_PORT
if __name__ == '__main__':
    start()
