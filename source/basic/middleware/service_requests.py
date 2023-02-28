# -*- coding: utf-8 -*-
"""
    >File   : service_requests.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/2/28 19:17
"""

import aiohttp
import json

from typing import Optional, List, Dict, Set
# from config import USER_SERVICE_PATH
from collections import defaultdict
from datetime import datetime
from pydantic import BaseModel, Field
# todo 后续集中config
from basic.config.monitor import *


class NotebookInfo(BaseModel):
    id: int
    name: str
    project_id: int
    status: str
    cpu: int
    memory: int
    gpu: int
    storage_value: int
    storage_size: int
    volume_ids: List[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
            'status': self.status,
            'cpu': self.cpu,
            'memory': self.memory,
            'gpu': self.gpu,
            'storage_value': self.storage_value,
            'storage_size': self.storage_size,
            'namespace_name': self.namespace_name,
            'pod_name': self.pod_name,
            'volume_ids': self.volume_ids,
        }


class JobInfo(BaseModel):
    id: int
    name: str
    project_id: int
    status: str
    volume_ids: List[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
            'status': self.status,
            'volume_ids': self.volume_ids,
        }


async def get_notebook_list(token, filter_path=None):
    res = []
    async with aiohttp.ClientSession() as session:
        url = f"http://{NOTEBOOK_SERVICE_URL}{NOTEBOOK_PREFIX_URL}/items"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        if filter_path:
            url += filter_path
        # print(url)
        async with session.get(url, headers=headers) as response:
            # print("status:{}".format(response.status))
            text = await response.json()
            note_data = text['result']
            for note in note_data:
                note['project_id'] = note['project']['id']
                res.append(NotebookInfo.parse_obj(note))
    return [x.get_dict() for x in res]


async def get_job_list(token, filter_path=None):
    res = []
    async with aiohttp.ClientSession() as session:
        url = f"http://{JOB_SERVICE_URL}{JOB_PREFIX_URL}/items"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        if filter_path:
            url += filter_path
        # print(url)
        async with session.get(url, headers=headers) as response:
            # print("status:{}".format(response.status))
            text = await response.json()
            job_data = text['result']
            # print(job_data)
            for job in job_data:
                job['project_id'] = job['project']['id']
                res.append(JobInfo.parse_obj(job))
    return [x.get_dict() for x in res]
