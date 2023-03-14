# -*- coding: utf-8 -*-
"""
    >File   : service_requests.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/2/17 15:15
"""

import aiohttp
from typing import Optional, List, Set
from pydantic import BaseModel
from basic.common.base_config import *
import requests


class PodInfoByServer(BaseModel):
    id: int
    name: str
    created_by_id: int
    cpu: int
    gpu: int
    memory: int
    created_by: str

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_by_id': self.created_by_id,
            'cpu': self.cpu,
            'gpu': self.gpu,
            'memory': self.memory,
            'created_by': self.created_by
        }


async def get_notebook_job_list_by_server(server_ip):
    res = []
    # response = requests.get(f"http://127.0.0.1:8012/notebooks/by_server/{server_ip}",
    #                         headers={'Content-Type': 'application/json'})
    response = requests.get(f"http://{NOTEBOOK_SERVICE_URL}{NOTEBOOK_PREFIX_URL}/by_server/{server_ip}",
                            headers={'Content-Type': 'application/json'})
    text_notebook = response.json()
    print(text_notebook)
    notebook_data = text_notebook['result']
    for note in notebook_data:
        print("``````````")
        print(note)
        print("``````````")
        res.append(PodInfoByServer.parse_obj(note))

    # response_job = requests.get(f"http://127.0.0.1:8013/jobs/by_server/{server_ip}",
    #                             headers={'Content-Type': 'application/json'})
    response_job = requests.get(f"http://{JOB_SERVICE_URL}{JOB_PREFIX_URL}/by_server/{server_ip}",
                                headers={'Content-Type': 'application/json'})
    text_job = response_job.json()
    job_data = text_job['result']
    for note in job_data:
        print("job``````````")
        print(note)
        print("job``````````")
        res.append(PodInfoByServer.parse_obj(note))
    return [x.get_dict() for x in res]
