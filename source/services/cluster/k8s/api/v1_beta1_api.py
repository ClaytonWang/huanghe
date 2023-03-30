from services.cluster.k8s.api.core import K8sConfigFactory


class V1Beta1Api:
    def __init__(self, kcf: K8sConfigFactory):
        self._kcf = kcf

    def v1_beta1_api(self, cluster=None):
        return self._kcf.get(key=cluster).v1_beta1_api
