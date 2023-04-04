# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, Dict, List
from basic.common.validator_name import BaseModelValidatorName


class Volume(BaseModel):
    name: str
    mount_path: str
    mount_propagation: Optional[str] = "HostToContainer"


class DeploymentCreateReq(BaseModelValidatorName):
    namespace: str
    image: str
    # 对应环境
    env: str = "dev"
    platform: str = "mvp"
    cpu: int = 0
    memory: int = 0
    gpu: int = 0
    volumes: List[Volume] = []
    tolerations: List[str] = []
    annotations: Dict = {}

    def gen_deployment_dict(self):
        return {
            "name": self.name,
            "namespace": self.namespace,
            "image": self.image,
            "labels": {"env": self.env, "app": self.name},
            "resource": {
                "cpu": self.cpu,
                "memory": f"{self.memory}Gi",
                "nvidia.com/gpu": self.gpu,
            },
            "cluster": self.cluster,
            "annotations": self.annotations,
            "volumes": [v.dict() for v in self.volumes]
        }


class DeploymentDeleteReq(BaseModelValidatorName):
    namespace: str


class DeploymentListReq(BaseModel):
    platform: str = "mvp"
    env: str
    namespace: str


class Deployment(BaseModelValidatorName):
    namespace: str
    image: str
    labels: Dict
    resource: Dict
    envs: Dict = {}
    volumes: List[Volume] = []
    tolerations: List[str] = []
    annotations: Dict = {}
