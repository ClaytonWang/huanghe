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
from starlette.authentication import AuthCredentials, SimpleUser
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose.jwt import JWTError


async def get_current_user(email=Optional[str]):
    from source.services.user.models import User
    return await User.objects.select_related('role').get_or_none(email=email)


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
            data = jwt.decode(token, key=SECRET_KEY)
            sub = data.get('sub') if 'sub' in data else ''
            sub and setattr(request, 'email', sub)

            userinfo = await get_current_user(sub)
            if userinfo:
                request.scope['user'] = userinfo
            else:
                return auth_error
            return await call_next(request)
        except JWTError:
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
