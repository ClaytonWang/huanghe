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
from typing import Optional
from config import DO_NOT_AUTH_URI
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose.jwt import JWTError
from pydantic import BaseModel, Field
import requests
import os

ENV_COMMON_URL = "http://121.36.41.231:32767/api/v1"
ACCOUNT_PREFIX_URL = "/user/user/account"
PROJECT_PREFIX_URL = "/user/project"
MOCK = os.getenv("MOCK_ACCOUNT_GETTER", False)
MOCK_USER_JSON = {"id": 60, 'username': "shouchen"}
MOCK_PROJECT_JSON = {"id": 1, "name": "决策平台"}
USER = "user"
ADMIN = "admin"
OWNER = "owner"


class Role(BaseModel):
    name: str


class AccountGetter(BaseModel):
    id: int = Field(..., alias='user_id')
    username: str = Field(..., alias='user_name')
    role: Role

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ProjectGetter(BaseModel):
    id: int = Field(..., alias='project_id')
    name: str = Field(..., alias='project_by')

    class Config:
        allow_population_by_field_name = True


async def get_current_user(token: str) -> AccountGetter:
    if MOCK:
        return AccountGetter.parse_obj(MOCK_USER_JSON)
    try:
        response = requests.get(f"{ENV_COMMON_URL}{ACCOUNT_PREFIX_URL}",
                                headers={"Authorization": token})
        json = response.json()
        ag = AccountGetter.parse_obj(json['result'])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='获取用户失败，请检查token')
    return ag


def get_project(token: str, project_id) -> ProjectGetter:
    try:
        response = requests.get(f"{ENV_COMMON_URL}{PROJECT_PREFIX_URL}/{project_id}",
                                headers={"Authorization": token}).json()
        project_dict = response['result']
        pg = ProjectGetter.parse_obj(project_dict)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='获取项目失败')
    return pg


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
