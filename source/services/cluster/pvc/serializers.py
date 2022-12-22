# -*- coding: utf-8 -*-

from pydantic import BaseModel, validator





class PVC(BaseModel):
    name: str
    namespace: str
    size: str
    # 对应环境
    env: str = "dev"



class PVCDeleteReq(BaseModel):
    name: str
    namespace: str