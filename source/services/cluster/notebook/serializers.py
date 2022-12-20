# -*- coding: utf-8 -*-

from pydantic import BaseModel





class NoteBook(BaseModel):
    name: str
    namespace: str
    image: str
    # 对应环境
    env: str = "dev"
    # 对应平台（决策、开放）
    platform: str = "mvp"

