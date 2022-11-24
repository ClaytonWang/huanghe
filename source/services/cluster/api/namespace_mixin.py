from __future__ import annotations
from core import Core
from model.v1_namespace import V1Namespace
from model.v1_status import V1Status

class NamespaceMixin:

    @classmethod
    def create_namespace(cls, c: Core, name: str):
        return cls._core_v1_api(c).create_namespace(body=V1Namespace.default(name=name))

    @classmethod
    def delete_namespace(cls, c: Core, name: str) -> V1Status:
        return cls._core_v1_api(c).delete_namespace(name=name)

    @staticmethod
    def _core_v1_api(c: Core):
        return c.core_v1_api
