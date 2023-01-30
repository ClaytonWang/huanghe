# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, Dict, List
from  basic.common.validator_name import  BaseModel_ValidatorName



class Volume(BaseModel):
    name: str
    mount_path: str
    mount_propagation: Optional[str] = "HostToContainer"



class VolcanoJobCreateReq(BaseModel_ValidatorName):
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
    command: List[str] = []
    working_dir: Optional[str] = None


    def gen_vcjob_dict(self):
        return {
            "name": self.name,
            "namespace": self.namespace,
            "image": self.image,
            "labels": {"env": self.env},
            "resource": {
                "cpu": self.cpu,
                "memory": f"{self.memory}Gi",
                "nvidia.com/gpu": self.gpu,
            },
            "volumes": [v.dict() for v in self.volumes],
            "command": self.command,
            "working_dir": self.working_dir,
        }

class VolcanoJobDeleteReq(BaseModel):
    name: str
    namespace: str

class VolcanoJobListReq(BaseModel):
    platform: str = "mvp"
    env: str

class VolcanoJob(BaseModel_ValidatorName):
    namespace: str
    image: str
    labels: Dict
    resource: Dict
    envs: Dict = {}
    volumes: List[Volume] = []
    tolerations: List[str] = []
    command: List[str] = []
    working_dir: Optional[str] = None
