# -*- coding: utf-8 -*-
"""
    >File    : views.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:10
"""
from fastapi import APIRouter, Depends, HTTPException, status
# from .models import User
from models.user import User
from api.services import hash_password
from api.serializers import UserList


router_user = APIRouter()


@router_user.post(
    '',
    description='创建用户',
    response_model=None,
)
async def create_user(user: UserList):
    user.password = hash_password(user.password)
    return await user.save()


@router_user.get(
    '',
    description='用户列表',
    response_model=UserList,
)
async def list_user(sort: str, filter: str, pageno: int = 1, pagesize: int = 10):
    """

    :param pageno:  页码
    :param pagesize:  容量
    :param sort: 排序
    :param filter: 过滤参数
    :return:
    """
    print(sort)
    print(filter)
    return await User.objects.paginate(page=pageno, page_size=pagesize).all()
    pass
