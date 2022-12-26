# -*- coding: utf-8 -*-
"""
    >File    : services.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/29 16:48
"""
from models import Role, User, Project, Permissions, OperationPms
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
    # 普通用户项目权限默认编辑
    edit_pms = await Permissions.objects.get_or_none(code='00030002')
    exist_pms = await OperationPms.objects.filter(project__in=project_ids, user=user).all()
    exist_ids = set([x.project.id for x in exist_pms])
    pms_list = []
    new_proj_ids = []
    for _project in projects:
        await _project.member.add(user)
        # 添加普通用户权限
        if _project.id not in exist_ids:
            pms_list.append(OperationPms(project=_project.id, user=user.id))
            new_proj_ids.append(_project.id)
    if pms_list:
        await OperationPms.objects.bulk_create(pms_list)
        add_pms = await OperationPms.objects.filter(project__in=new_proj_ids, user=user).all()
        for _pms in add_pms:
            await _pms.permissions.add(edit_pms)
