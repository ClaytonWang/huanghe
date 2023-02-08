# -*- coding: utf-8 -*-
"""
    >File   : k8s_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/22 18:58
"""

import json

import aiohttp
from fastapi import HTTPException, status
from pydantic import BaseModel

from basic.common.env_variable import get_string_variable
# from config import K8S_SERVICE_PATH
from basic.config.job_management import *


class PVCCreateReq(BaseModel):
    name: str
    namespace: str
    size: str
    # 对应环境
    env: str = "dev"


async def create_job_k8s(token, payloads):
    async with aiohttp.ClientSession() as session:
        # url = K8S_SERVICE_PATH + "/job"
        # url = ENV_COMMON_URL + CLUSTER_JOB_PREFIX_URL
        url = f"http://{CLUSTER_SERVICE_URL}{CLUSTER_JOB_PREFIX_URL}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.post(url, headers=headers, data=payloads) as response:
            print("status:{}".format(response.status))
            response = await response.json()
            # print(response)
            return response['status']


async def delete_job_k8s(token, payloads):
    async with aiohttp.ClientSession() as session:
        # url = K8S_SERVICE_PATH + "/job"
        # url = ENV_COMMON_URL + CLUSTER_JOB_PREFIX_URL
        url = f"http://{CLUSTER_SERVICE_URL}{CLUSTER_JOB_PREFIX_URL}"
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        async with session.delete(url, headers=headers, data=payloads) as response:
            print("status:{}".format(response.status))
            response = await response.json()
            # print(response)
            return response['status']


class JobListReq(BaseModel):
    env: str = get_string_variable('ENV', 'DEV').lower()


async def list_job_k8s(nblr: JobListReq):
    async with aiohttp.ClientSession() as session:
        # url = K8S_SERVICE_PATH + "/job/batch"
        # url = f"{ENV_COMMON_URL}{CLUSTER_JOB_PREFIX_URL}/batch"
        url = f"http://{CLUSTER_SERVICE_URL}{CLUSTER_JOB_PREFIX_URL}/batch"
        headers = {
            'Content-Type': 'application/json'
        }
        async with session.post(url, headers=headers, data=json.dumps(nblr.dict())) as response:
            # print("status:{}".format(response.status))
            response = await response.json()
            # print(response)
            return response['result']


async def create_pvc(pvc: PVCCreateReq, ignore_exist=False):
    async with aiohttp.ClientSession() as session:
        url = f"http://{CLUSTER_SERVICE_URL}{CLUSTER_PVC_PREFIX_URL}"
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            async with session.post(url, headers=headers, data=json.dumps(pvc.dict())) as response:
                # print("status:{}".format(response.status))
                response = await response.json()
                # print(response)
                if ignore_exist and response["success"] is not True and response["message"] == "AlreadyExists":
                    return True
                assert response['success'] is True
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='创建pvc失败, 请确认是否存在namespace， 或者pvc是否已经存在')
        return True


# def list_job_k8s(nblr: JobListReq):
#     try:
#         response = requests.post(f"{K8S_SERVICE_PATH}/job/batch", json=nblr.dict()).json()
#         assert response['success'] is True
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='批量查询job失败')
#     return response["result"]


# if __name__ == '__main__':
#     res = list_job_k8s(JobListReq())
#     print(res)
