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
        if path:
            load_kube_config(path)
        elif os.getenv("KUBECONFIG"):
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


kubeconfig_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "kubeconfig")


class K8sConfigFactory:
    pool = {}

    def __init__(self):
        if not self.pool:
            for file in os.listdir(kubeconfig_path):
                self.pool[file] = Core(os.path.join(kubeconfig_path, file))
        self.pool["default"] = Core()


    def __getitem__(self, item):
        return self.pool[item]

    def get(self, key=None) -> Core:
        return self.pool[key]

kcf = K8sConfigFactory()