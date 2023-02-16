import aiohttp
from basic.config.monitor import *

async def list_server_k8s():
    async with aiohttp.ClientSession() as session:
        # url = "http://127.0.0.1:8001/server"
        url = f"{ENV_COMMON_URL}{CLUSTER_SERVER_PREFIX_URL}"
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        async with session.get(url) as response:
            response = await response.json()
            return response['result']