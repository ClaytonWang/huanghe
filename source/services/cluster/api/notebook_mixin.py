from __future__ import annotations
from core import Core
from model.v1_status import V1Status
from api.custom_object_api import CustomerObjectApi
from const.crd_kubeflow_const import KUBEFLOW_NOTEBOOK_GROUP, KUBEFLOW_V1_VERSION, KUBEFLOW_NOTEBOOK_PLURAL
from model.v1_notebook import V1Notebook
from typing import Dict

class NotebookMixin(CustomerObjectApi):

    @classmethod
    def create_notebook(cls, c: Core, name: str, namespace: str, image: str) -> Dict:
        return cls.custom_object_api(c).create_namespaced_custom_object(group=KUBEFLOW_NOTEBOOK_GROUP,
                                                                        version=KUBEFLOW_V1_VERSION,
                                                                        namespace=namespace,
                                                                        plural=KUBEFLOW_NOTEBOOK_PLURAL,
                                                                        body=V1Notebook.default(name=name,
                                                                                                namespace=namespace,
                                                                                                image=image),
                                                                        )

    @classmethod
    def delete_notebook(cls, c: Core, name: str, namespace: str) -> V1Status:
        return cls.custom_object_api(c).delete_namespaced_custom_object(name=name, namespace=namespace)

    @classmethod
    def list_notebook(cls, c):
        return cls.custom_object_api(c).list_namespaced_custom_object()

    @classmethod
    def watch_notebook(cls, c):
        return cls.custom_object_api(c).list_cluster_custom_object(group=KUBEFLOW_NOTEBOOK_GROUP,
                                                                        version=KUBEFLOW_V1_VERSION,
                                                                        plural=KUBEFLOW_NOTEBOOK_PLURAL,
                                                                        watch=True)