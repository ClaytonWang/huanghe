# -*- coding: utf-8 -*-
"""
    >File   : notebook_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/2/20 16:29
"""
import aiohttp
from pydantic import BaseModel
from basic.common.base_config import *


class SourceInfo(BaseModel):
    id: int
    name: str


async def get_source_list(token):
    async with aiohttp.ClientSession() as session:
        url = f"http://{NOTEBOOK_SERVICE_URL}{NOTEBOOK_SOURCE_PREFIX_URL}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            # print("status:{}".format(response.status))
            text = await response.json()
            result = text['result']
            return result


async def get_image_list(token):
    async with aiohttp.ClientSession() as session:
        url = f"http://{NOTEBOOK_SERVICE_URL}{NOTEBOOK_IMAGE_PREFIX_URL}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            # print("status:{}".format(response.status))
            text = await response.json()
            result = text['result']
            # print(job_data)
            return result
