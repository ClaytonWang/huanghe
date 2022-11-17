# -*- coding: utf-8 -*-
"""
    >File    : views.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:10
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from apps.auth.services import verify_password, create_access_token
from apps.auth.serializers import Token
from models import User


router_auth = APIRouter()


@router_auth.post(
    "/login",
    response_model=Token,
    description='登录',
    response_description="返回access_token"
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1、获取客户端传过来的用户名、密码
    username = form_data.username
    password = form_data.password
    # 2、验证用户
    user = await User.objects.get(username=username)
    if not verify_password(password, user.password):
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user)
    # 4、生成 token
    access_token = create_access_token(data={"sub": user.username})
    # 5、返回 JSON 响应
    return {"access_token": access_token, "token_type": "bearer"}


async def access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    pass
