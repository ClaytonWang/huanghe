# -*- coding: utf-8 -*-
"""
    >File    : auth.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/12 09:24
"""
from jose import jwt
from fastapi import Request, Response, status
from settings import SECRET_KEY


async def verify_token(request: Request, call_next):
    auth_error = Response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    path: str = request.get('path')
    # 登录接口、docs文档依赖的接口，不做token校验
    if path.startswith('/auth/login') | path.startswith('/docs') | path.startswith('/openapi'):
        return await call_next(request)
    else:
        try:
            # 从header读取token
            authorization: str = request.headers.get('authorization')
            if not authorization:
                return auth_error

            token = authorization.split(' ')[1]
            jwt.decode(token, key=SECRET_KEY)
            return await call_next(request)
        except Exception as e:
            print(e)
            return auth_error
