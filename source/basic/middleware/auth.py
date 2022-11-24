# -*- coding: utf-8 -*-
"""
    >File    : token.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/23 13:17
"""
from jose import jwt
from fastapi import Request, Response, status
from fastapi import HTTPException
from typing import Optional
from config import SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.exceptions import ValidationError
from fastapi.exception_handlers import http_exception_handler


async def verify_token(request: Request, call_next):
    auth_error = Response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    path: str = request.get('path')
    # 登录接口、docs文档依赖的接口，不做token校验
    if path.startswith('/v1/auth/login') | \
            path.startswith('/docs') | \
            path.startswith('/openapi'):
        return await call_next(request)
    else:
        try:
            # 从header读取token
            authorization: str = request.headers.get('authorization')
            if not authorization:
                return auth_error

            token = authorization.split(' ')[1]
            jwt.decode(token, key=SECRET_KEY)

            # 参数已经需要重新封装
            try:
                return await call_next(request)
            except ValidationError as exc:
                exc.status_code = 400
                setattr(exc, 'detail', str(exc))
                return await http_exception_handler(request, exc)
        except Exception as e:
            print(e)
            return auth_error


class OFOAuth2PasswordBearer(OAuth2PasswordBearer):
    """"""

    def __init__(self, token_url: str):
        super().__init__(
            tokenUrl=token_url,
            scheme_name=None,
            scopes=None,
            description=None,
            auto_error=True
        )

    async def __call__(self, request: Request) -> Optional[str]:
        path: str = request.get('path')
        if path.startswith('/v1/auth/login') \
                | path.startswith('/docs') \
                | path.startswith('/openapi'):
            return ""
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param
