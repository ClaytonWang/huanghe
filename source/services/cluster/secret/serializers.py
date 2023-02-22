# -*- coding: utf-8 -*-

from pydantic import BaseModel


class SecretCommon(BaseModel):
    name: str
    namespace: str


class SecretNamespace(BaseModel):
    namespace: str
