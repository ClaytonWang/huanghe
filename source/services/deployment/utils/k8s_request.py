# -*- coding: utf-8 -*-
"""
    >File   : k8s_request.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/22 18:58
"""

import ujson as json

import aiohttp
from pydantic import BaseModel
import requests

from basic.common.env_variable import get_string_variable
from fastapi import Request, Response, status
from fastapi import HTTPException
from services.deployment.deployment.serializers import DeploymentList, DeploymentCreate, DeploymentDetail, \
    DeploymentEdit, DeploymentOp, DeploymentStatusUpdate, DeploymentDeleteReq, DeploymentCreateReq, \
    DeploymentListReq, DeploymentItem, ServiceCreateReq, ServiceDeleteReq, ServiceQuery
from config import *

import pprint


class JobListReq(BaseModel):
    env: str = get_string_variable('ENV', 'DEV').lower()


def create_deploy_k8s(deploymentc: DeploymentCreateReq, ignore_exist=False):
    try:
        # response = requests.post(f"http://127.0.0.1:8003/job", json=vjc.dict()).json()
        print("deploymentc")
        pprint.pprint(deploymentc.dict())
        response = requests.post(
            f"http://{CLUSTER_SERVICE_URL}{CLUSTER_DEPLOYMENT_PREFIX_URL}", json=deploymentc.dict()).json()
        if ignore_exist and response["success"] is not True and response["message"] == "AlreadyExists":
            return True
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='创建deployment失败')
    return True


def delete_deploy_k8s(deploymentd: DeploymentDeleteReq, ignore_no_found=False):
    try:
        response = requests.delete(
            f"http://{CLUSTER_SERVICE_URL}{CLUSTER_DEPLOYMENT_PREFIX_URL}", json=deploymentd.dict()).json()
        if ignore_no_found and response["success"] is not True and response["message"] == "NotFound":
            return True
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除deployment失败')
    return True


def create_service(servicec: ServiceCreateReq, ignore_exist=False):
    try:
        # response = requests.post(f"http://127.0.0.1:8003/job", json=vjc.dict()).json()
        response = requests.post(
            f"http://{CLUSTER_SERVICE_URL}{CLUSTER_SERVICE_PREFIX_URL}", json=servicec.dict()).json()
        if ignore_exist and response["success"] is not True and response["message"] == "AlreadyExists":
            return True
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='创建service失败')
    return True


def list_service(serviceq: ServiceQuery):
    try:
        # response = requests.post(f"http://127.0.0.1:8003/job", json=vjc.dict()).json()
        response = requests.post(
            f"http://{CLUSTER_SERVICE_URL}{CLUSTER_SERVICE_PREFIX_URL}/batch", json=serviceq.dict()).json()
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='创建service失败')
    return response['result']


def delete_service(serviced: ServiceDeleteReq, ignore_no_found=False):
    try:
        response = requests.delete(
            f"http://{CLUSTER_SERVICE_URL}{CLUSTER_SERVICE_PREFIX_URL}", json=serviced.dict()).json()
        if ignore_no_found and response["success"] is not True and response["message"] == "NotFound":
            return True
        assert response['success'] is True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除service失败')
    return True


def generate_service_payloads(payloads):
    """
    生成service的payloads
    Returns:

    """
    def get_new_cluster_ip(cluster_ips):
        if not cluster_ips:
            # 没有情况下随便返回一个
            return '10.247.164.139'
        cluster_ips.sort()
        max_cluster = cluster_ips[-1]
        cluster_int = max_cluster.split('.')
        for i in range(3, -1, -1):
            if cluster_int[i] != '255':
                cluster_int[i] = str(int(cluster_int[i]) + 1)
                break
        # 这里极端情况255.255.255.255无法生成
        return '.'.join(cluster_int)

    # print(ServiceQuery.parse_raw(payloads))
    service_list = list_service(ServiceQuery.parse_raw(payloads))
    # pprint.pprint(service_list)
    cluster_ips = [x['cluster_ip'] for x in service_list]
    # print(f"cluster_ips: {cluster_ips}")
    new_cluster_ip = get_new_cluster_ip(cluster_ips)
    _payloads = {
        **json.loads(payloads),
        "cluster_ip": new_cluster_ip,
        "port": 80
    }
    return json.dumps(_payloads)


def create_deploy_k8s_pipeline(payloads, ignore_exist=False):
    # 创建deployment
    create_deploy_k8s(deploymentc=DeploymentCreateReq.parse_raw(payloads), ignore_exist=ignore_exist)
    # 创建service
    service_payloads = generate_service_payloads(payloads)
    create_service(servicec=ServiceCreateReq.parse_raw(service_payloads), ignore_exist=ignore_exist)
    return True


def delete_deploy_k8s_pipeline(payloads, ignore_no_found=False):
    # 删除deployment
    delete_deploy_k8s(deploymentd=DeploymentDeleteReq.parse_raw(payloads), ignore_no_found=ignore_no_found)
    # 删除service
    delete_service(serviced=ServiceDeleteReq.parse_raw(payloads), ignore_no_found=ignore_no_found)
    return True
