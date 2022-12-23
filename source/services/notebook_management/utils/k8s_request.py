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
from models.notebook import Status, Notebook


async def update_start_notebook(token):
    async with aiohttp.ClientSession() as session:
        url = K8S_SERVICE_PATH + "/user/account"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            print("status:{}".format(response.status))
            text = await response.json()
            # print(text)
            # return text
            stat = await Status.objects.get(name='start')
            _notebook = await Notebook.objects.filter(status_id=stat.id)
            return _notebook
