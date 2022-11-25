# -*- coding: utf-8 -*-
"""
    >File    : permissions_services.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/25 13:10
"""
import re
from models import Permissions
from models import Role
SINGLE_LAYER_MENU_LENGTH = 4


async def generate_code(parent_code: str, project: str = None) -> (bool, str):
    """
    :param parent_code:
    :param project:
    :return:
    """
    print('parent: ', parent_code)
    query = Permissions.objects.filter()
    if project:
        query = query.filter(project=project)

    if parent_code:
        if not await Permissions.objects.filter(code=parent_code).exists():
            return False, 'Not Query ParentCode'

        query = await query.filter(code__startswith=parent_code)\
            .order_by('-code').values(fields=['id', 'code'])
        if len(query) == 1:
            return True, parent_code + str(1).zfill(SINGLE_LAYER_MENU_LENGTH)
        else:
            same_query = [
                item for item in query if len(item['code']) == len(parent_code)
                + SINGLE_LAYER_MENU_LENGTH
            ]
            reg_str = '.{' + str(SINGLE_LAYER_MENU_LENGTH) + '}'
            codes = re.findall(reg_str, same_query[0]['code'])
            code = str(int(codes[-1]) + 1).zfill(SINGLE_LAYER_MENU_LENGTH)
            new_code = ''.join(codes[:-1]) + code
            return True, new_code
    else:
        query = await query.order_by('-code').values(fields=['id', 'code'])
        if not query:
            return True, str(1).zfill(SINGLE_LAYER_MENU_LENGTH)
        else:
            same_query = [
                item for item in query
                if len(item['code']) == SINGLE_LAYER_MENU_LENGTH
            ]
            code = str(int(same_query[0]['code']) + 1).zfill(
                SINGLE_LAYER_MENU_LENGTH
            )
            return True, code


def join_pms_item(menu, desc=[], level=1):
    """
    返回嵌套接口
    :param menu:
    :param desc:
    :param level:
    :return:
    """
    layer = SINGLE_LAYER_MENU_LENGTH * level
    menu_id = menu.get('code')
    next_menu_id = menu_id[layer:]
    parent_id = menu_id[:layer+SINGLE_LAYER_MENU_LENGTH]
    if len(next_menu_id) == SINGLE_LAYER_MENU_LENGTH:
        menu['children'] = []
        if desc:
            desc.append(menu)
        else:
            desc = [menu]
        return desc
    else:
        for _index, _item in enumerate(desc):
            if parent_id != str(_item.get('code')):
                continue
            desc[_index]['children'] = join_pms_item(
                menu, _item.get('children'),
                level=int(len(parent_id)/SINGLE_LAYER_MENU_LENGTH)
            )
        return desc


def join_pms_to_string(pms, parent_value=None) -> list:
    """
    权限因子 嵌套接口->字符拼接
    :param pms:
    :param parent_value:
    :return:
    """
    result = []
    for item in pms:
        value = item['value']
        if parent_value:
            new_value = f'{parent_value}.{value}'
            result.append(new_value)
        else:
            new_value = value
            result.append(f'{value}')

        children = item.get('children', [])
        if children:
            result += join_pms_to_string(children, parent_value=new_value)
    return result


async def role_pms(role: str) -> list:
    """
    根据角色查询缺陷因子
    :param role:
    :return:
    """
    pms = await Permissions.objects.filter(
        role__name=role
    ).order_by('code').fields(['code', 'name', 'value']).values()

    order_pms = sorted(pms, key=lambda item: int(item['code']))
    results = []
    for _item in order_pms:
        results = join_pms_item(_item, results, level=0)

    return join_pms_to_string(results)
