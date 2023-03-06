# -*- coding: utf-8 -*-
"""
    >File   : auth.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/20 17:42
"""

from fastapi import Request, Response, status
from config import DO_NOT_AUTH_URI
from jose.jwt import JWTError
from utils.user_request import get_current_user_aio, get_project
from services.job_management.models.job import Job

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
            # print("that's it token")
            # print(authorization)
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


async def operate_auth(request: Request, job_id: int):
    _job = await Job.objects.select_related('status').get_or_none(pk=job_id)
    if not _job:
        return None, 'Job不存在'
    # 正确返回job
    if _job.created_by_id == request.user.id or request.user.role.name == 'admin':
        return _job, None
    # 普通用户
    if request.user.role.name == 'user':
        permissions = request.user.permissions
        if {'jobs.list.create', 'jobs.list.edit', 'jobs.list.delete'}.issubset(permissions):
            return None, '不能编辑非自己创建的Job'
        else:
            return None, '用户没有编辑权限'
    # 项目负责人
    stat, _project = await get_project(request.headers.get('authorization'), _job.project_id)
    if stat != 200:
        return None, '项目不存在'
    owner_id = _project['owner']['id']
    if int(owner_id) != request.user.id:
        return None, '不能编辑非自己负责的Job'
    return _job, None
