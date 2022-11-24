from __future__ import annotations
from core import Core
from model.v1_status import V1Status
from api.custom_object_api import CustomerObjectApi

class NotebookMixin(CustomerObjectApi):

    @classmethod
    def create_notebook(cls, c: Core):
        return cls.custom_object_api(c).create_namespaced_custom_object()

    @classmethod
    def delete_notebook(cls, c: Core, name: str, namespace: str) -> V1Status:
        return cls.custom_object_api(c).delete_namespaced_custom_object(name=name, namespace=namespace)

    @classmethod
    def list_notebook(cls, c):
        return cls.custom_object_api(c).list_namespaced_custom_object()
