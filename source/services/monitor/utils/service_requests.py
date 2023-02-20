# -*- coding: utf-8 -*-
"""
    >File   : service_requests.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/2/17 15:15
"""


import aiohttp
import json

from typing import Optional, List, Dict, Set
# from config import USER_SERVICE_PATH
from collections import defaultdict
from datetime import datetime
from pydantic import BaseModel, Field
from basic.config.monitor import *


class RoleInfo(BaseModel):
    id: int
    name: str


class UserInfo(BaseModel):
    id: int = Field(..., alias='user_id')
    username: str = Field(..., alias='user_name')
    en_name: str = Field(..., )
    role: RoleInfo
    permissions: Optional[List[str]]
    project_ids: Set

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "en_name": self.en_name,
            "role_id": self.role.id,
            "role_name": self.role.name,
            "permissions": self.permissions,
            "project_ids": self.project_ids,
        }


class NotebookInfo(BaseModel):
    id: int
    name: str
    project_id: int
    status: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
            'status': self.status,
        }


class JobInfo(BaseModel):
    id: int
    name: str
    project_id: int
    status: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
            'status': self.status,
        }


async def get_user_list(token):
    async with aiohttp.ClientSession() as session:
        # url = USER_SERVICE_PATH + f"/user?pagesize=100&pageno={page_no}"
        # url = f"{ENV_COMMON_URL}{USER_PREFIX_URL}/items"
        url = f"http://{USER_SERVICE_URL}{USER_PREFIX_URL}/items"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            # print("status:{}".format(response.status))
            text = await response.json()
            user_data = text['result']
            res = []
            for user in user_data:
                projects = user.pop('projects')
                user['project_ids'] = {x["id"] for x in projects}
                res.append(UserInfo.parse_obj(user))
            return [x.get_dict() for x in res]


async def get_notebook_list(token, filter_path=None):
    res = []
    async with aiohttp.ClientSession() as session:
        # url = f"{ENV_COMMON_URL}{NOTEBOOK_PREFIX_URL}?filter[project__code]={project_code}"
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
        # url = f"{ENV_COMMON_URL}{NOTEBOOK_PREFIX_URL}?filter[project__code]={project_code}"
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