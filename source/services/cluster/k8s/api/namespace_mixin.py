from __future__ import annotations
from services.cluster.k8s.api.core import Core
from services.cluster.k8s.api.core_v1_api import CoreV1Api
from services.cluster.k8s.model.v1_namespace import V1Namespace
from services.cluster.k8s.model.v1_status import V1Status
from namespace.serializers import Namespace


class NamespaceMixin(CoreV1Api):
    def __init__(self, c: Core):
        super(NamespaceMixin, self).__init__(c=c)

    def create_namespace(self, ns: Namespace) -> V1Namespace:
        return self.core_v1_api.create_namespace(body=V1Namespace.default(name=ns.name, labels=ns.labels))

    def delete_namespace(self, ns: Namespace) -> V1Status:
        return self.core_v1_api.delete_namespace(name=ns.name)
