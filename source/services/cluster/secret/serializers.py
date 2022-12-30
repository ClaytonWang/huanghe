# -*- coding: utf-8 -*-

from pydantic import BaseModel, validator
from typing import Dict



class SecretCommon(BaseModel):
    name: str
    namespace: str



class SecretNamespace(BaseModel):
    namespace: str


