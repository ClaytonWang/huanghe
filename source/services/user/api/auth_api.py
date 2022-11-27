# -*- coding: utf-8 -*-
"""
    >File    : auth_api.py.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/21 20:16
"""
from fastapi import APIRouter, HTTPException, status
from api.services import verify_password, create_access_token
from models.user import User
from api.serializers import Token
from api.serializers import Login


router_auth = APIRouter()


@router_auth.post(
    "/login",
    response_model=Token,
    description='登录',
    response_description="返回access_token"
)
async def login(body: Login):
    user = await User.objects.get_or_none(email=body.email)
    if not user or not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"token": access_token, "token_type": "bearer"}


@router_auth.put(
    '/logout',
    description='退出',
    responses={status.HTTP_204_NO_CONTENT: {'model': None}}
)
def logout():
    pass

