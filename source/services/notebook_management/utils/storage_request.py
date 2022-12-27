# -*- coding: utf-8 -*-
"""
    >File   : storage_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/21 16:35
"""

import aiohttp
import json

from typing import List, Dict
from config import STORAGE_SERVICE_PATH
from collections import defaultdict
from pydantic import BaseModel, Field


class VolumeConfigInfo(BaseModel):
    value: int
    size: int

    def vol_config(self):
        return {
            "value": self.value,
            "size": self.size,
        }


class VolumeInfo(BaseModel):
    id: int = Field(..., alias='volume_id')
    name: str = Field(..., alias='volume_name')
    config: VolumeConfigInfo

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "config": self.config.vol_config(),
        }


async def get_volume_list(token, page_no=1):
    res = []
    async with aiohttp.ClientSession() as session:
        url = STORAGE_SERVICE_PATH + f"/volume?pagesize=100&pageno={page_no}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            print("status:{}".format(response.status))
            text = await response.json()
            # print(text)
            volume_data = text['result']['data']
            for vol in volume_data:
                res.append(VolumeInfo.parse_obj(vol))
    return [x.get_dict() for x in res]


async def volume_check(authorization: str, hooks: List[Dict]):
    volume_list = await get_volume_list(authorization)
    volume_map = {x['id']: x for x in volume_list}
    storages = []
    volumes_k8s = []

    for hook in hooks:
        volume_id = hook['volume_id']
        path = hook['path']
        volume_info = volume_map.get(volume_id)
        volumes_k8s.append({'name': volume_info['name'], 'mount_path': path})
        storages.append({'storage': volume_info, 'path': path})
    return storages, volumes_k8s
