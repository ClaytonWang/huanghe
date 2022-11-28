from __future__ import annotations
from core import Core
from api.core_v1_api import CoreV1Api
from model.v1_namespace import V1Namespace
from model.v1_status import V1Status

class NamespaceMixin(CoreV1Api):

    @classmethod
    def create_namespace(cls, c: Core, name: str):
        return cls.core_v1_api(c).create_namespace(body=V1Namespace.default(name=name))

    @classmethod
    def delete_namespace(cls, c: Core, name: str) -> V1Status:
        return cls.core_v1_api(c).delete_namespace(name=name)

