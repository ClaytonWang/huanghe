# -*- coding: utf-8 -*-
"""
    >File    : permissions_init.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/25 09:35
"""
from models.user import Role
from models.permissions import Permissions


def pms_data():
    # admin owner  user
    data = [
        {
            'name': 'bam',
            'value': '后台模块',
            'access': ['admin'],
            'children': [
                {
                    'name': 'projects',
                    'value': '项目列表',
                    'access': ['admin'],
                    'children': [
                        {
                            'name': 'create',
                            'value': '创建',
                            'access': ['admin'],
                        },
                        {
                            'name': 'edit',
                            'value': '编辑',
                            'access': ['admin'],
                        },
                        {
                            'name': 'delete',
                            'value': '删除',
                            'access': ['admin'],
                        }
                    ]
                },
                {
                    'name': 'users',
                    'value': '用户列表',
                    'access': ['admin'],
                    'children': [
                        {
                            'name': 'create',
                            'value': '创建',
                            'access': ['admin'],
                        },
                        {
                            'name': 'edit',
                            'value': '编辑',
                            'access': ['admin'],
                        },
                        {
                            'name': 'delete',
                            'value': '删除',
                            'access': ['admin'],
                        }
                    ]
                }
            ]
        },
        {
            'name': 'settings',
            'value': '设置',
            'access': ['owner'],
            'children': [
                {
                    'name': 'users',
                    'value': '用户列表',
                    'access': ['owner'],
                    'children': [
                        {
                            'name': 'create',
                            'value': '新建',
                            'access': ['owner'],
                        },
                        {
                            'name': 'edit',
                            'value': '编辑',
                            'access': ['owner'],
                        },
                        {
                            'name': 'delete',
                            'value': '删除',
                            'access': ['owner'],
                        },
                    ]
                },
            ]
        },
        {
            'name': 'project',
            'value': '项目',
            'access': [],
            'children': [
                {
                    'name': 'readonly',
                    'value': '新建',
                    'access': [],
                },
                {
                    'name': 'edit',
                    'value': '编辑',
                    'access': [],
                }
            ]
        }
    ]
    return data


async def add_data(pms, parent_code=None):

    from permissions.services import generate_code

    for item in pms:
        if item['name'] == '设置':
            print('name: ', item['name'])
        state, code = await generate_code(parent_code=parent_code)
        print(state, code)
        kwargs = dict(
            name=item['name'],
            value=item['value'],
            # created_by_id=1,
            code=code,
        )
        access = item['access']
        new = await Permissions.objects.create(**kwargs)
        for acc in access:
            role = await Role.objects.filter(name=acc).first()
            await new.role.add(role)

        children = item.get('children')
        if children:
            await add_data(children, new.code)


async def init_pms():
    await add_data(pms_data())


if __name__ == '__main__':
    pass
