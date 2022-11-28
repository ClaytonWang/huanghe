"""
启动入口、根路由配置
"""
import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/status')
def status():
    return {"status": "ok"}


def start():
    service_port = int(os.getenv('CLUSTER_SERVICE_PORT', 80))
    uvicorn.run(
        'main:app', host='0.0.0.0', port=service_port,
        reload=False,
        # debug=DEBUG,
        workers=2
    )

# USER_SERVICE_PORT
if __name__ == '__main__':
    start()
