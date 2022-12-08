"""
启动入口、根路由配置
"""
import os
import uvicorn
from fastapi import FastAPI
from volume.api import router_volume
from models import startup_event, shutdown_event

app = FastAPI()


@app.get('/status')
def status():
    return {"status": "ok"}

app.include_router(router_volume, prefix="/volume")


# 配置数据库连接
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

def start():
    service_port = int(os.getenv('VOLUME_SERVICE_PORT', 8001))
    uvicorn.run(
        'main:app', port=service_port,
        reload=False,
        # debug=DEBUG,
        workers=2
    )

# USER_SERVICE_PORT
if __name__ == '__main__':
    start()
