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
            'name': '后台模块',
            'value': 'bam',
            'access': ['admin'],
            'children': [
                {
                    'name': '项目列表',
                    'value': 'projects',
                    'access': ['admin'],
                    'children': [
                        {
                            'name': '创建',
                            'value': 'create',
                            'access': ['admin'],
                        },
                        {
                            'name': '编辑',
                            'value': 'edit',
                            'access': ['admin'],
                        },
                        {
                            'name': '删除',
                            'value': 'delete',
                            'access': ['admin'],
                        }
                    ]
                },
                {
                    'name': '用户列表',
                    'value': 'users',
                    'access': ['admin'],
                    'children': [
                        {
                            'name': '创建',
                            'value': 'create',
                            'access': ['admin'],
                        },
                        {
                            'name': '编辑',
                            'value': 'edit',
                            'access': ['admin'],
                        },
                        {
                            'name': '删除',
                            'value': 'delete',
                            'access': ['admin'],
                        }
                    ]
                }
            ]
        },
        {
            'name': '设置',
            'value': 'settings',
            'access': ['owner'],
            'children': [
                {
                    'name': '用户列表',
                    'value': 'users',
                    'access': ['owner'],
                    'children': [
                        {
                            'name': '新建',
                            'value': 'create',
                            'access': ['owner'],
                        },
                        {
                            'name': '编辑',
                            'value': 'edit',
                            'access': ['owner'],
                        },
                        {
                            'name': '删除',
                            'value': 'delete',
                            'access': ['owner'],
                        },
                    ]
                },
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
