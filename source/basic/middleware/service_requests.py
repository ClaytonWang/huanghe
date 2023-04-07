# -*- coding: utf-8 -*-
"""
    >File   : service_requests.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/2/28 19:17
"""

import aiohttp

import json

from fastapi import HTTPException, status
from typing import Optional, List, Set
from pydantic import BaseModel, Field
from basic.common.base_config import *


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


class PVCCreateReq(BaseModel):
    name: str
    namespace: str
    size: str
    # 对应环境
    env: str = "dev"


class Storage(BaseModel):
    name: Optional[str]
    id: int


class HookItem(BaseModel):
    storage: Storage
    path: str


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
    creator_en_name: str = Field(..., alias='creator_en_name')
    config: VolumeConfigInfo

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'creator_en_name': self.creator_en_name,
            'config': self.config.vol_config(),
        }


class SourceInfo(BaseModel):
    id: int
    name: str


async def get_user_list(token):
    """
    获取用户全量列表
    Args:
        token:

    Returns:

    """
    async with aiohttp.ClientSession() as session:
        url = f"http://{USER_SERVICE_URL}{USER_ITEMS_URL}"
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
    """
    获取项目全量列表
    Args:
        token:

    Returns:

    """
    async with aiohttp.ClientSession() as session:
        url = f"http://{USER_SERVICE_URL}{PROJECT_ITEMS_URL}"
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


async def get_notebook_list(token, filter_path=None):
    """
    获取notebook全量列表
    Args:
        token:
        filter_path:

    Returns:

    """
    async with aiohttp.ClientSession() as session:
        url = f"http://{NOTEBOOK_SERVICE_URL}{NOTEBOOK_ITEMS_URL}"
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
            res = []
            for note in note_data:
                note['project_id'] = note['project']['id']
                res.append(NotebookInfo.parse_obj(note))
            return [x.get_dict() for x in res]


async def get_job_list(token, filter_path=None):
    """
    获取job全量列表
    Args:
        token:
        filter_path:

    Returns:

    """
    async with aiohttp.ClientSession() as session:
        url = f"http://{JOB_SERVICE_URL}{JOB_ITEMS_URL}"
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
            res = []
            for job in job_data:
                job['project_id'] = job['project']['id']
                res.append(JobInfo.parse_obj(job))
            return [x.get_dict() for x in res]


async def create_pvc(pvc: PVCCreateReq, ignore_exist=False):
    """
    创建pvc
    Args:
        pvc:
        ignore_exist:

    Returns:

    """
    async with aiohttp.ClientSession() as session:
        url = f"http://{CLUSTER_SERVICE_URL}{CLUSTER_PVC_PREFIX_URL}"
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            async with session.post(url, headers=headers, data=json.dumps(pvc.dict())) as response:
                # print("status:{}".format(response.status))
                response = await response.json()
                # print(response)
                if ignore_exist and response["success"] is not True and response["message"] == "AlreadyExists":
                    return True
                assert response['success'] is True
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='创建pvc失败, 请确认是否存在namespace， 或者pvc是否已经存在')
        return True


async def get_volume_list(token, page_no=1):
    """
    获取存储卷列表
    Args:
        token:
        page_no:

    Returns:

    """
    res = []
    async with aiohttp.ClientSession() as session:
        url = f"http://{STORAGE_SERVICE_URL}{VOLUME_PREFIX_URL}?pagesize=100&pageno={page_no}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.get(url, headers=headers) as response:
            # print("status:{}".format(response.status))
            text = await response.json()
            # print(text)
            volume_data = text['result']['data']
            for vol in volume_data:
                vol['creator_en_name'] = vol['creator']['en_name']
                res.append(VolumeInfo.parse_obj(vol))
    return [x.get_dict() for x in res]


async def volume_check(authorization: str, hooks: List[HookItem], namespace: str):
    """
    存储卷校验
    Args:
        authorization:
        hooks:
        namespace:

    Returns:

    """
    storages, volumes_k8s = [], []
    if not hooks:
        return storages, volumes_k8s
    volume_list = await get_volume_list(authorization)
    volume_map = {int(x['id']): x for x in volume_list}

    for hook in hooks:
        path = hook.path
        volume_info = volume_map.get(int(hook.storage.id))
        volume_k8s_name = f"{volume_info['creator_en_name']}-{volume_info['name']}"
        volumes_k8s.append({'name': volume_k8s_name, 'mount_path': path})
        storages.append({'storage': volume_info, 'path': path})
        # 校验创建pvc
        await create_pvc(PVCCreateReq(name=volume_k8s_name, namespace=namespace,
                                      size=volume_info['config']['size'], env=ENV),
                         ignore_exist=True)

    if len(set(x['path'] for x in storages)) != len(storages):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='同一个NoteBook中挂载的目录不能重复')

    return storages, volumes_k8s


async def get_project(token, proj_id):
    """
    获取单个project信息
    Args:
        token:
        proj_id:

    Returns:

    """
    async with aiohttp.ClientSession() as session:
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


async def get_source_list(token):
    """
    获取资源列表
    Args:
        token:

    Returns:

    """
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
    """
    获取镜像列表
    Args:
        token:

    Returns:

    """
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
