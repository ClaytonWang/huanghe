# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, Dict, List
from basic.common.validator_name import BaseModelValidatorName, Cluster


class Volume(BaseModel):
    name: str
    mount_path: str
    mount_propagation: Optional[str] = "HostToContainer"


class NoteBookCreateReq(BaseModelValidatorName):
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

    def gen_notebook_dict(self):
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
            "annotations": self.annotations,
            "volumes": [v.dict() for v in self.volumes]
        }


class NoteBookDeleteReq(BaseModelValidatorName):
    namespace: str


class NoteBookListReq(Cluster):
    platform: str = "mvp"
    env: str


class NoteBook(BaseModelValidatorName):
    namespace: str
    image: str
    labels: Dict
    resource: Dict
    envs: Dict = {}
    volumes: List[Volume] = []
    tolerations: List[str] = []
    annotations: Dict = {}
