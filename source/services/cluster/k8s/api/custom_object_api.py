from services.cluster.k8s.api.core import Core


class CustomerObjectApi:
    def __init__(self, c: Core):
        self._c = c

    @property
    def custom_object_api(self):
        return self._c.custom_object_api
