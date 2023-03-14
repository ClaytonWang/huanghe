# -*- coding: utf-8 -*-
"""
    >File   : user_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/19 10:14
"""

import aiohttp

from config import *
from basic.middleware.service_requests import get_project


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
