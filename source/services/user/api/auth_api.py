# -*- coding: utf-8 -*-
"""
    >File    : auth_api.py.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/21 20:16
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .services import verify_password, create_access_token
# from .models import User
from models.user import User
from .serializers import Token
from api.serializers import LoginBody


router_auth = APIRouter()


@router_auth.post(
    "/login",
    response_model=Token,
    description='登录',
    response_description="返回access_token"
)
async def login(body: LoginBody):
    # 1、获取客户端传过来的用户名、密码
    # 2、验证用户
    user = await User.objects.get(username=body.username)
    if not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 4、生成 token
    access_token = create_access_token(data={"sub": user.username})
    # 5、返回 JSON 响应
    return {"access_token": access_token, "token_type": "bearer"}


