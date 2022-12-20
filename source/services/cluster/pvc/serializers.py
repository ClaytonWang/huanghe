# -*- coding: utf-8 -*-

from pydantic import BaseModel





class PVC(BaseModel):
    name: str
    namespace: str
    size: str
    # 对应环境
    env: str = "dev"
    # 对应平台（决策、开放）
    platform: str = "mvp"



class PVCDeleteReq(BaseModel):
    name: str
    namespace: str