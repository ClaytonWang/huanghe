# -*- coding: utf-8 -*-
"""
    >File    : token.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/23 13:17
"""
from __future__ import annotations
from fastapi import Request, Response, status
from fastapi import HTTPException
from typing import Optional, List, Dict
from config import DO_NOT_AUTH_URI
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose.jwt import JWTError
from pydantic import BaseModel, Field, validator
import requests
import os
from basic.config.storage import *

class ProjectGetter(BaseModel):
    id: int = Field(..., alias='project_id')
    name: str = Field(..., alias='project_by')
    en_name: str
    class Config:
        allow_population_by_field_name = True

    @validator("en_name")
    def name_match(cls, en_name: str):
        ans = []
        for ch in en_name:
            if ch == "-":
                ans.append(ch)
            if ch.isalpha() or ch.isdigit():
                ans.append(ch.lower())
        return ''.join(ans)

class SecretNamespace(BaseModel):
    namespace: str

class PVCCreateReq(BaseModel):
    name: str
    namespace: str
    size: str
    # 对应环境
    env: str = "dev"


class PVCDeleteReq(BaseModel):
    name: str
    namespace: str

class Namespace(BaseModel):
    name: str

    @validator("name")
    def name_match(cls, name: str):
        ans = []
        for ch in name:
            if ch == "-":
                ans.append(ch)
            if ch.isalpha() or ch.isdigit():
                ans.append(ch.lower())
        return ''.join(ans)

class Role(BaseModel):
    name: str


class AccountGetter(BaseModel):
    id: int = Field(..., alias='user_id')
    username: str = Field(..., alias='user_name')
    en_name: str
    role: Role
    projects: List[ProjectGetter]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    @validator("en_name")
    def name_match(cls, en_name: str):
        ans = []
        for ch in en_name:
            if ch.isalpha() or ch.isdigit():
                ans.append(ch.lower())
        return ''.join(ans)


async def get_current_user(token: str) -> AccountGetter:
    if MOCK:
        return AccountGetter.parse_obj(MOCK_USER_JSON)
    try:

        response = requests.get(f"http://{USER_SERVICE_URL}{ACCOUNT_PREFIX_URL}",
                                headers={"Authorization": token})
        json = response.json()
        ag = AccountGetter.parse_obj(json['result'])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='获取用户失败，请检查token')
    return ag


def get_project(token: str, project_id) -> ProjectGetter:
    try:
        response = requests.get(f"http://{USER_SERVICE_URL}{PROJECT_PREFIX_URL}/{project_id}",
                                headers={"Authorization": token}).json()
        project_dict = response['result']
        pg = ProjectGetter.parse_obj(project_dict)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='获取项目失败')
    return pg

def create_secret(sn: SecretNamespace, ignore_exist=False):
    try:
        response = requests.post(f"http://{CLUSTER_SERVICE_URL}{CLUSTER_SECRET_PREFIX_URL}", json=sn.dict()).json()
        if ignore_exist and response["success"] is not True and response["message"] == "AlreadyExists":
            return True
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='创建secret失败, 请确认是否存在namespace， 或者secret是否已经存在')

    return True
def create_pvc(pvc: PVCCreateReq, ignore_exist=False):
    try:
        response = requests.post(f"http://{CLUSTER_SERVICE_URL}{CLUSTER_PVC_PREFIX_URL}", json=pvc.dict()).json()
        if ignore_exist and response["success"] is not True and response["message"] == "AlreadyExists":
            return True
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='创建pvc失败, 请确认是否存在namespace， 或者pvc是否已经存在')

    return True

def delete_pvc(pvc: PVCDeleteReq):
    try:
        response = requests.delete(f"http://{CLUSTER_SERVICE_URL}{CLUSTER_PVC_PREFIX_URL}", json=pvc.dict()).json()
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除pvc失败, 请确认是否存在namespace， 或者pvc是否不存在')
    return True

def create_ns(ns: Namespace):
    try:
        response = requests.post(f"http://{CLUSTER_SERVICE_URL}{CLUSTER_NAMESPACE_PREFIX_URL}", json=ns.dict()).json()
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='创建namespace失败')
    return True


def delete_ns(ns: Namespace):
    try:

        response = requests.delete(f"http://{CLUSTER_SERVICE_URL}{CLUSTER_NAMESPACE_PREFIX_URL}", json=ns.dict()).json()
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除namespace失败')
    return True

def query_notebook_volume(token: str, volume_id) -> List[Dict]:
    # http://{USER_SERVICE_URL}{PROJECT_PREFIX_URL}/{project_id}
    try:
        response = requests.get(f"{ENV_COMMON_URL}{NOTEBOOK_VOLUME_PREFIX_URL}/{volume_id}", headers={"Authorization": token}).json()
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='查询notebook存储盘失败')
    return response['result']



async def verify_token(request: Request, call_next):
    auth_error = Response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    path: str = request.get('path')
    # 登录接口、docs文档依赖的接口，不做token校验
    if path in DO_NOT_AUTH_URI:
        return await call_next(request)
    else:
        try:
            # 从header读取token
            authorization: str = request.headers.get('authorization')
            if not authorization:
                return auth_error

            userinfo = await get_current_user(authorization)
            if userinfo:
                request.scope['user'] = userinfo
            else:
                return auth_error
            return await call_next(request)
        except JWTError:
            return auth_error


class OFOAuth2PasswordBearer(OAuth2PasswordBearer):
    """"""

    def __init__(self, token_url: str):
        super().__init__(
            tokenUrl=token_url,
            scheme_name=None,
            scopes=None,
            description=None,
            auto_error=True
        )

    async def __call__(self, request: Request) -> Optional[str]:
        path: str = request.get('path')
        if path in DO_NOT_AUTH_URI:
            return ""
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


