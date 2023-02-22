import os
from kubernetes.config import load_kube_config, load_incluster_config
from kubernetes.client import CoreV1Api, CustomObjectsApi, StorageV1Api


class Core:
    def __init__(self):
        self._find_kubeconfig()
        self._core_v1_api = CoreV1Api()
        self._custom_object_api = CustomObjectsApi()
        self._storage_v1_api = StorageV1Api()

    def _find_kubeconfig(self):
        if os.getenv("KUBECONFIG"):
            load_kube_config()
        else:
            load_incluster_config()

    @property
    def core_v1_api(self):
        return self._core_v1_api

    @property
    def custom_object_api(self):
        return self._custom_object_api

    @property
    def storage_v1_api(self):
        return self._storage_v1_api
