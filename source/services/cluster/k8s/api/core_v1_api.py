from k8s.api.core import Core

class CoreV1Api():
    def __init__(self, c: Core):
        self._c = c

    @property
    def core_v1_api(self):
        return self._c.core_v1_api
