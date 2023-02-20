# -*- coding: utf-8 -*-
"""
    >File   : notebook_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/2/20 16:29
"""
import aiohttp
import json

from typing import Optional, List, Dict, Set
from collections import defaultdict
from pydantic import BaseModel, Field
from basic.config.job_management import *


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
            source_data = text['result']["data"]
            # print(job_data)
            return source_data
