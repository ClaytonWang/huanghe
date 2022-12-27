# -*- coding: utf-8 -*-
"""
    >File   : user_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/19 10:14
"""

import aiohttp
import json

from typing import List, Dict
from config import USER_SERVICE_PATH
from collections import defaultdict
from pydantic import BaseModel, Field


class RoleInfo(BaseModel):
    id: int
    name: str


class UserInfo(BaseModel):
    id: int = Field(..., alias='user_id')
    username: str = Field(..., alias='user_name')
    en_name: str = Field(..., )
    role: RoleInfo
    project_ids: Dict

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

# def get_auth_token():
#     url = f"{USER_SERVICE_PATH}/auth/login"
#     payload = json.dumps({
#         "username": "admin",
#         "password": "admin123",
#         "email": "admin@admin.com"
#     })
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     if response.status_code != 200:
#         print('报错')
#         return
#
#     res_json = response.json()['result']
#     return f"{res_json['token_type']} {res_json['token']}"


async def get_current_user_aio(token):
    async with aiohttp.ClientSession() as session:
        url = USER_SERVICE_PATH + "/user/account"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            print("status:{}".format(response.status))
            text = await response.json()
            # print(text)
            # return text
            user_dict = text['result']
            projects = user_dict.pop('projects')
            user_dict['project_ids'] = {x["id"]: x["en_name"] for x in projects}
            userinfo = UserInfo.parse_obj(user_dict)
            return userinfo


async def get_user_list(token, page_no=1):
    res = []
    async with aiohttp.ClientSession() as session:
        # TODO 分页器目前限制100，超过100后报错，用户项目多后会有问题（也可以反复循环到result为空）
        url = USER_SERVICE_PATH + f"/user?pagesize=100&pageno={page_no}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            print("status:{}".format(response.status))
            text = await response.json()
            user_data = text['result']['data']
            for user in user_data:
                projects = user.pop('projects')
                user['project_ids'] = {x["id"]: x["en_name"] for x in projects}
                res.append(UserInfo.parse_obj(user))
            # print(text)
    return [x.get_dict() for x in res]


async def get_project_list(token, page_no=1):
    res = []
    async with aiohttp.ClientSession() as session:
        url = USER_SERVICE_PATH + f"/project?pagesize=100&pageno={page_no}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            print("status:{}".format(response.status))
            text = await response.json()
            # print(text)
            proj_data = text['result']['data']
            for proj in proj_data:
                res.append(ProjectInfo.parse_obj(proj))
    return [x.get_dict() for x in res]


async def get_project(token, proj_id):
    async with aiohttp.ClientSession() as session:
        url = USER_SERVICE_PATH + f"/project/{proj_id}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            print("status:{}".format(response.status))
            text = await response.json()
            print(text)
            return text['result']

