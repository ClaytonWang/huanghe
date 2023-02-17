# -*- coding: utf-8 -*-
"""
    >File   : user_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/19 10:14
"""

import aiohttp
import json

from typing import Optional, List, Dict, Set
# from config import USER_SERVICE_PATH
from collections import defaultdict
from pydantic import BaseModel, Field
from basic.config.job_management import *


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


class ProjectInfo(BaseModel):
    id: int = Field(..., alias='project_id')
    code: str = Field(..., )
    name: str = Field(..., alias='project_by')
    en_name: str = Field(..., )

    class Config:
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "en_name": self.en_name,
        }


async def get_current_user_aio(token):
    async with aiohttp.ClientSession() as session:
        # url = USER_SERVICE_PATH + "/user/account"
        # url = ENV_COMMON_URL + ACCOUNT_PREFIX_URL
        url = f"http://{USER_SERVICE_URL}{ACCOUNT_PREFIX_URL}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            # print("status:{}".format(response.status))
            # 把401传递出去
            if response.status != 200:
                return None
            text = await response.json()
            # print(text)
            # return text
            user_dict = text['result']
            projects = user_dict.pop('projects')
            user_dict['project_ids'] = {x["id"] for x in projects}
            userinfo = UserInfo.parse_obj(user_dict)
            return userinfo


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


async def get_project_list(token):
    async with aiohttp.ClientSession() as session:
        # url = USER_SERVICE_PATH + f"/project?pagesize=100&pageno={page_no}"
        # url = f"{ENV_COMMON_URL}{PROJECT_PREFIX_URL}/items"
        url = f"http://{USER_SERVICE_URL}{PROJECT_PREFIX_URL}/items"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            # print("status:{}".format(response.status))
            text = await response.json()
            # print(text)
            proj_data = text['result']
            res = []
            for proj in proj_data:
                res.append(ProjectInfo.parse_obj(proj))
            return [x.get_dict() for x in res]


async def get_project(token, proj_id):
    async with aiohttp.ClientSession() as session:
        # url = USER_SERVICE_PATH + f"/project/{proj_id}"
        # url = f"{ENV_COMMON_URL}{PROJECT_PREFIX_URL}/{proj_id}"
        url = f"http://{USER_SERVICE_URL}{PROJECT_PREFIX_URL}/{proj_id}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            # print("status:{}".format(response.status))
            text = await response.json()
            # print(text)
            return text['status'], text['result']


async def project_check(request, project_id):
    if request.user.role.name != 'admin' and project_id not in [project.id for project in request.user.projects]:
        return False, '不是用户所属项目'
    stat, proj = await get_project(request.headers.get('authorization'), project_id)
    if stat != 200:
        return False, '项目不存在'
    return True, proj['en_name']


async def project_check_obj(request, project_id):
    if request.user.role.name != 'admin' and project_id not in [project.id for project in request.user.projects]:
        return False, '不是用户所属项目'
    stat, proj = await get_project(request.headers.get('authorization'), project_id)
    if stat != 200:
        return False, '项目不存在'
    return True, proj
