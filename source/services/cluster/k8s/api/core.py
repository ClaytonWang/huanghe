import os
from kubernetes.config import load_kube_config, load_incluster_config
from kubernetes.client import CoreV1Api, CustomObjectsApi, StorageV1Api, AppsV1Api


class Core:
    def __init__(self, path=None):
        self._find_kubeconfig(path)
        self._core_v1_api = CoreV1Api()
        self._custom_object_api = CustomObjectsApi()
        self._storage_v1_api = StorageV1Api()
        self._apps_v1_api = AppsV1Api()

    def _find_kubeconfig(self, path=None):
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

    @property
    def apps_v1_api(self):
        return self._apps_v1_api