# -*- coding: utf-8 -*-
"""
    >File   : service_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/1/4 15:34
"""

import aiohttp
import requests

from typing import Optional, List, Dict, Set
# from config import USER_SERVICE_PATH
from collections import defaultdict
from datetime import datetime
from pydantic import BaseModel, Field
from config import *


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
    owner_id: int
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id,
            'deleted_at': self.deleted_at,
        }


async def get_notebook_list(token, project_code, username=None):
    res = []
    async with aiohttp.ClientSession() as session:
        # url = f"{ENV_COMMON_URL}{NOTEBOOK_PREFIX_URL}?filter[project__code]={project_code}"
        url = f"http://{NOTEBOOK_SERVICE_URL}{NOTEBOOK_PREFIX_URL}?filter[project__code]={project_code}"
        if username:
            url += f"&filter[username]={username}"
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
        # url = f"{ENV_COMMON_URL}{VOLUME_PREFIX_URL}"
        url = f"http://{STORAGE_SERVICE_URL}{VOLUME_PREFIX_URL}"
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
                vol['owner_id'] = vol['owner']['id']
                res.append(VolumeInfo.parse_obj(vol))
    return [x.get_dict() for x in res]


def query_job_by_project(token: str, project_id: int, user_id: Optional[int] = None) -> bool:
    try:
        response = requests.get(f"http://{JOB_SERVICE_URL}{JOB_PREFIX_URL}/{project_id}?user_id={user_id}" if user_id
                                else f"http://{JOB_SERVICE_URL}{JOB_PREFIX_URL}/{project_id}",
                                headers={"Authorization": token})
        response = response.json()
        assert response['success'] is True
    except Exception as e:
        raise e
    return response['result']


def query_notebook_by_project(token: str, project_id: int, user_id: Optional[int] = None) -> bool:
    try:
        response = requests.get(
            f"http://{NOTEBOOK_SERVICE_URL}{NOTEBOOK_BACK_PREFIX_URL}/{project_id}?user_id={user_id}" if user_id else
            f"http://{NOTEBOOK_SERVICE_URL}{NOTEBOOK_BACK_PREFIX_URL}/{project_id}",
            headers={"Authorization": token})
        response = response.json()
        assert response['success'] is True
    except Exception as e:
        raise e
    return response['result']
