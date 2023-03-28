from services.cluster.k8s.api.core import K8sConfigFactory


class CustomerObjectApi:
    def __init__(self, kcf: K8sConfigFactory):
        self._kcf = kcf

    def custom_object_api(self, cluster=None):
        return self._kcf.get(key=cluster).custom_object_api
