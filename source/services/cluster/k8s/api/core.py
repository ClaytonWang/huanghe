from kubernetes.config import load_kube_config
from kubernetes.client import CoreV1Api, CustomObjectsApi, StorageV1Api

class Core():
    def __init__(self):
        load_kube_config("/Users/jiangshouchen/Downloads/config")
        self._core_v1_api = CoreV1Api()
        self._custom_object_api = CustomObjectsApi()
        self._storage_v1_api = StorageV1Api()

    @property
    def core_v1_api(self):
        return self._core_v1_api

    @property
    def custom_object_api(self):
        return self._custom_object_api

    @property
    def storage_v1_api(self):
        return self._storage_v1_api


if __name__ == '__main__':
    c = Core()
    l = c.core_v1_api.list_namespaced_pod("default")
    print(l)