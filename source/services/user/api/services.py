# -*- coding: utf-8 -*-
"""
    >File    : services.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/10/13 07:10
"""
from jose import jwt
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Request, Response, status
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password: str) -> str:
    """
    密码加密
    :param password:
    :return:
    """
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password, hashed_password):
    """
    验证密码
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(
        data: dict,
        expires_minutes: Optional[int] = None):
    """
    用户名、密码验证成功后，生成 token
    :param data:
    :param expires_minutes:
    :return:
    """
    to_encode = data.copy()
    if expires_minutes:
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
