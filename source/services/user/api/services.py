# -*- coding: utf-8 -*-
"""
    >File    : services.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/29 16:48
"""
from models import Role, User, Project
from typing import List


async def update_user_of_project(project_ids: List[int], user: User, delete_old: bool = False):
    """
    更新项目成员，

    删掉所有旧的重新添加，TODO：已经存在的不删除重新添加，新增新加，删除去掉
    :param project_ids:
    :param user:
    :param delete_old: 删除旧数据
    :return:
    """
    # TODO 异常回滚
    if delete_old:
        await user.projects.clear()

    projects = await Project.objects.filter(id__in=project_ids).all()
    for _project in projects:
        await _project.member.add(user)
