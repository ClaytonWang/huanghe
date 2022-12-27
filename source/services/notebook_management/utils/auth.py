# -*- coding: utf-8 -*-
"""
    >File   : auth.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/20 17:42
"""
import json

from jose import jwt
from fastapi import Request, Response, status
from fastapi import HTTPException
from typing import Optional
from config import DO_NOT_AUTH_URI
from starlette.authentication import AuthCredentials, SimpleUser
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose.jwt import JWTError
from utils.user_request import get_current_user_aio, get_project
from models import Notebook


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
            print("that's it token")
            print(authorization)
            if not authorization:
                return auth_error

            userinfo = await get_current_user_aio(authorization)
            # print(type(userinfo))
            # print(userinfo)

            if userinfo:
                request.scope['user'] = userinfo
            else:
                return auth_error
            return await call_next(request)
        except JWTError:
            return auth_error


async def operate_auth(request: Request, notebook_id: int):
    _notebook = await Notebook.objects.select_related('status').get_or_none(pk=notebook_id)
    if not _notebook:
        return None, 'Notebook不存在'
    # 正确返回notebook
    if _notebook.creator_id == request.user.id or request.user.role.name == 'admin':
        return _notebook, None
    # 普通用户
    if request.user.role.name == 'user':
        return None, '不能编辑非自己创建的Notebook'
    # 项目负责人
    _project = await get_project(request.headers.get('authorization'), _notebook.project_id)
    owner_id = _project['owner']['id']
    if int(owner_id) != request.user.role.id:
        return None, '不能编辑非自己负责的Notebook'
    return _notebook, None
