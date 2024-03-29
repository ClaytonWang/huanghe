# -*- coding: utf-8 -*-
"""
    >File   : serializers.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/20 15:37
"""
import re
from datetime import datetime
from fastapi import HTTPException, status
from typing import Optional, List, Union, Dict

from pydantic import BaseModel, Field
from pydantic import validator

from basic.utils.dt_format import dt_to_string
from basic.common.validator_name import BaseModelValidatorName


def k8s_format(name):
    if not name or not re.match('^[a-z][0-9a-z-]*$', name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Deployment命名必须为小写英文字母数字中划线组合,且首位必须是字母')
    return name.lower()


class StatusItem(BaseModel):
    code: str = None
    name: str = None
    desc: str = None


class UserStr(BaseModel):
    id: int
    username: str = None


class ProjectStr(BaseModel):
    id: int
    name: Optional[str] = None



class JobOp(BaseModel):
    action: int


class Creator(BaseModel):
    id: str
    username: str


class Project(BaseModel):
    id: int
    name: Optional[str]


class Image(BaseModel):
    name: str
    desc: Optional[str] = ""
    custom: Optional[bool] = True


class SourceItem(BaseModel):
    id: int
    name: str


class UrlAddress(BaseModel):
    type: str
    address: str



class DeploymentList(BaseModel):
    id: int
    status: StatusItem
    name: str
    source: Optional[str]
    creator: Optional[UserStr]
    project: Optional[ProjectStr]
    image: Image
    # url: Optional[str]
    created_at: Union[datetime, str, None]
    updated_at: Union[datetime, str, None]
    # private_ip: str
    # public_ip: str
    # port: int
    urls: List[UrlAddress]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        if isinstance(dt, str):
            return dt
        return dt_to_string(dt, '%Y-%m-%d')


class DeploymentCreate(BaseModel):
    name: str = Field(..., max_length=20)
    project: Project
    source: str
    image: Image
    # private_ip: str
    # public_ip: str
    # port: int

    @validator('name')
    def deployment_name_validator(cls, name):
        return k8s_format(name)


class DeploymentDetail(BaseModel):
    id: int
    name: str
    creator: Creator
    created_at: Union[datetime, str, None]
    status: StatusItem
    project: Project
    image: Image
    source: str = None
    updated_at: Union[datetime, str, None]
    urls: List[UrlAddress]

    @validator('created_at', 'updated_at')
    def format_dt(cls, dt):
        if isinstance(dt, str):
            return dt
        return dt_to_string(dt, '%Y-%m-%d')


class DeploymentEdit(BaseModel):
    project: Project
    image: Image
    work_dir: Optional[str]
    source: str


class DeploymentOp(BaseModel):
    action: int


class StatusItemOnlyDesc(BaseModel):
    desc: str = None


class DeploymentStatusUpdate(BaseModel):
    status: str
    server_ip: Optional[str]


class EventItem(BaseModel):
    id: Optional[int]
    status: StatusItemOnlyDesc
    name: Optional[str] = ""
    time: Optional[datetime]


class EventCreate(BaseModel):
    name: str
    desc: str
    source_id: int
    source: Optional[str] = "VCDEPLOYMENT"


class DeploymentStatusUpdate(BaseModel):
    status: str
    server_ip: Optional[str]


class Volume(BaseModel):
    name: str
    mount_path: str
    mount_propagation: Optional[str] = "HostToContainer"


# 部署部分
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
            "annotations": self.annotations,
            "volumes": [v.dict() for v in self.volumes]
        }


class DeploymentDeleteReq(BaseModel):
    name: str
    namespace: str


class DeploymentListReq(BaseModel):
    platform: str = "mvp"
    env: str
    namespace: str


class DeploymentItem(BaseModelValidatorName):
    namespace: str
    image: str
    labels: Dict
    resource: Dict
    envs: Dict = {}
    volumes: List[Volume] = []
    tolerations: List[str] = []
    annotations: Dict = {}


# 服务部分
class ServiceCreateReq(BaseModelValidatorName):
    name: str
    namespace: str
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


class ServiceDeleteReq(BaseModel):
    name: str
    namespace: str


class ServiceQuery(BaseModel):
    namespace: str
