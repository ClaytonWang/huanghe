# -*- coding: utf-8 -*-
"""
    >File   : k8s_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/22 18:58
"""

import aiohttp
import json

from typing import List
from config import K8S_SERVICE_PATH


async def create_notebook_k8s(token, payloads):
    async with aiohttp.ClientSession() as session:
        url = K8S_SERVICE_PATH + "/notebook"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.post(url, headers=headers, payloads=payloads) as response:
            print("status:{}".format(response.status))
            response = await response.json()
            return response.status


