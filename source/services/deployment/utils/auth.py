# -*- coding: utf-8 -*-
"""
    >File   : auth.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/20 17:42
"""

from fastapi import Request
from basic.middleware.service_requests import get_project
from services.deployment.models import Deployment


async def operate_auth(request: Request, job_id: int):
    _deploy = await Deployment.objects.select_related('status').get_or_none(pk=job_id)
    if not _deploy:
        return None, 'Deployment'
    # 正确返回_deploy
    if _deploy.created_by_id == request.user.id or request.user.role.name == 'admin':
        return _deploy, None
    # 普通用户
    if request.user.role.name == 'user':
        permissions = request.user.permissions
        if {'jobs.list.create', 'jobs.list.edit', 'jobs.list.delete'}.issubset(permissions):
            return None, '不能编辑非自己创建的Deployment'
        else:
            return None, '用户没有编辑权限'
    # 项目负责人
    stat, _project = await get_project(request.headers.get('authorization'), _deploy.project_id)
    if stat != 200:
        return None, '项目不存在'
    owner_id = _project['owner']['id']
    if int(owner_id) != request.user.id:
        return None, '不能编辑非自己负责的Deployment'
    return _deploy, None
