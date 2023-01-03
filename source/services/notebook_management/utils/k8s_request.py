# -*- coding: utf-8 -*-
"""
    >File   : k8s_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/22 18:58
"""

import aiohttp
import json
from fastapi import HTTPException, status
from basic.common.env_variable import get_string_variable
from pydantic import BaseModel
from typing import List
from config import K8S_SERVICE_PATH


async def create_notebook_k8s(token, payloads):
    async with aiohttp.ClientSession() as session:
        url = K8S_SERVICE_PATH + "/notebook"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.post(url, headers=headers, data=payloads) as response:
            print("status:{}".format(response.status))
            response = await response.json()
            # print(response)
            return response['status']


async def delete_notebook_k8s(token, payloads):
    async with aiohttp.ClientSession() as session:
        url = K8S_SERVICE_PATH + "/notebook"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.delete(url, headers=headers, data=payloads) as response:
            print("status:{}".format(response.status))
            response = await response.json()
            # print(response)
            return response['status']


class NoteBookListReq(BaseModel):
    env: str = get_string_variable('ENV', 'DEV').lower()


async def list_notebook_k8s(nblr: NoteBookListReq):
    async with aiohttp.ClientSession() as session:
        url = K8S_SERVICE_PATH + "/notebook/batch"
        headers = {
            'Content-Type': 'application/json'
        }
        async with session.post(url, headers=headers, data=json.dumps(nblr.dict())) as response:
            print("status:{}".format(response.status))
            response = await response.json()
            # print(response)
            return response['result']


# def list_notebook_k8s(nblr: NoteBookListReq):
#     try:
#         response = requests.post(f"{K8S_SERVICE_PATH}/notebook/batch", json=nblr.dict()).json()
#         assert response['success'] is True
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='批量查询notebook失败')
#     return response["result"]


if __name__ == '__main__':
    res = list_notebook_k8s(NoteBookListReq())
    print(res)
