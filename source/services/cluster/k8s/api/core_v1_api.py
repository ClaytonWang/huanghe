from services.cluster.k8s.api.core import K8sConfigFactory


class CoreV1Api:
    def __init__(self, kcf: K8sConfigFactory):
        self._kcf = kcf


    def core_v1_api(self, cluster=None):
        return self._kcf.get(cluster).core_v1_api
