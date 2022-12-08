# -*- coding: utf-8 -*-

from pydantic import BaseModel


class Volume(BaseModel):
    name: str


class VolumeList(BaseModel):
    id: int
    name: str

# class VolumeCreate(BaseModel):
#     username: str = Field(..., max_length=80)
#     current: int = Field(..., )
#     limit: int = Field()
#     owner: str = Field
#     project: Optional[List[int]] = []
#     is_delete: bool = Field
#
#     @validator('password')
#     def set_password(cls, pwd):
#         return hash_password(pwd)






