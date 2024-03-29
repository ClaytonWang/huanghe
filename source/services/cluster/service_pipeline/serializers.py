# -*- coding: utf-8 -*-
"""
    >File   : serializers.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/14 15:49
"""
from pydantic import BaseModel
from typing import Optional
from services.cluster.deployment.serializers import Deployment, DeploymentCreateReq
from services.cluster.service.serializers import Service, ServiceCreateReq
from services.cluster.ingress.serializers import Ingress
from basic.common.validator_name import BaseModelValidatorName

class Volume(BaseModel):
    name: str
    mount_path: str
    mount_propagation: Optional[str] = "HostToContainer"

class ServicePipelineCreateReq(DeploymentCreateReq, ServiceCreateReq, Ingress):

    def gen_service_pipeline_dict(self):
        d = self.gen_service_dict()
        d.update(self.gen_deployment_dict())
        return d


class ServicePipelineDeleteReq(BaseModelValidatorName):
    namespace: str


class ServicePipeline(Service, Deployment, Ingress):

    def gen_service(self) -> Service:
        return Service.parse_obj(self)

    def gen_deployment(self) -> Deployment:
        return Deployment.parse_obj(self)

    def gen_ingress(self) -> Ingress:
        return Ingress.parse_obj(self)


if __name__ == '__main__':
    sp = ServicePipeline(name="test", namespace="test", image="test", labels={},
                         resource={}, envs={}, cluster_ip="123", ports=[])
    t = sp.gen_service()
    print(t)
    print(type(t))