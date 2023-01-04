# -*- coding: utf-8 -*-
"""
    >File   : service_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/1/4 15:34
"""

import aiohttp
import json

from typing import Optional, List, Dict, Set
# from config import USER_SERVICE_PATH
from collections import defaultdict
from pydantic import BaseModel, Field
from basic.config.user import *


class NotebookInfo(BaseModel):
    id: int
    name: str
    project_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
        }


class VolumeInfo(BaseModel):
    id: int = Field(..., alias='volume_id')
    name: str = Field(..., alias='volume_name')
    project_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
        }


async def get_notebook_list(token, project_code):
    res = []
    async with aiohttp.ClientSession() as session:
        url = f"{ENV_COMMON_URL}{NOTEBOOK_PREFIX_URL}?filter[project__code]={project_code}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            print("status:{}".format(response.status))
            text = await response.json()
            note_data = text['result']['data']
            for note in note_data:
                note['project_id'] = note['project']['id']
                res.append(NotebookInfo.parse_obj(note))
    return [x.get_dict() for x in res]


async def get_volume_list(token):
    res = []
    async with aiohttp.ClientSession() as session:
        url = f"{ENV_COMMON_URL}{VOLUME_PREFIX_URL}"
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
                vol['project_id'] = vol['project']['id']
                res.append(VolumeInfo.parse_obj(vol))
    return [x.get_dict() for x in res]

