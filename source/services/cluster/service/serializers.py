# -*- coding: utf-8 -*-
"""
    >File   : serializers.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/14 15:49
"""
from pydantic import BaseModel
from basic.common.validator_name import BaseModelValidatorName, Cluster
from typing import Dict, List


class ServiceCreateReq(BaseModelValidatorName):
    name: str
    namespace: str
    # image: str
    # 对应环境
    env: str = "dev"
    annotations: Dict = {}
    cluster_ip: str
    port: int

    def gen_service_dict(self):
        return {
            "name": self.name,
            "namespace": self.namespace,
            # "image": self.image,
            "labels": {"env": self.env, "app": self.name},
            "annotations": self.annotations,
            "cluster_ip": self.cluster_ip,
            "ports": [{"name": self.name, "port": self.port}],
            "selector": {"app": self.name}
        }


class ServiceDeleteReq(BaseModelValidatorName):
    name: str
    namespace: str


class Service(BaseModelValidatorName):
    namespace: str
    # image: str
    labels: Dict
    annotations: Dict = {}
    cluster_ip: str
    ports: List
    selector: Dict = {}


class ServiceQuery(Cluster):
    namespace: str
    env: str
