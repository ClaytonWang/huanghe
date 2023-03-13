import aiohttp
from basic.common.base_config import *

async def list_server_ip_k8s():
    async with aiohttp.ClientSession() as session:
        # url = "http://127.0.0.1:8010/server"
        url = f"http://{CLUSTER_SERVICE_URL}{CLUSTER_SERVER_PREFIX_URL}"
        headers = {
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return response['result']