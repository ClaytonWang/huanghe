from services.cluster.k8s.api.core import K8sConfigFactory


class AppsV1Api:
    def __init__(self, kcf: K8sConfigFactory):
        self._kcf = kcf

    def apps_v1_api(self, cluster: str = None):
        return self._kcf.get(cluster).apps_v1_api
