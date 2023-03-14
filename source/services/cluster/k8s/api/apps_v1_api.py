from services.cluster.k8s.api.core import Core


class AppsV1Api:
    def __init__(self, c: Core):
        self._c = c

    @property
    def apps_v1_api(self):
        return self._c.apps_v1_api
