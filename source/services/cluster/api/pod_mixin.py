from __future__ import annotations
from core import Core
from core_v1_api import CoreV1Api
from model.v1_pod import V1Pod

class PodMixin(CoreV1Api):
    @classmethod
    def list_namespaced_pod(cls, c: Core):
        return cls.core_v1_api(c).list_namespaced_pod()

    @classmethod
    def create_namespaced_pod(cls, c: Core, namespace: str, name: str, image: str):
        return cls.core_v1_api(c).create_namespaced_pod(namespace, body=V1Pod.default(name=name,
                                                                                      namespace=namespace,
                                                                                      image=image))



