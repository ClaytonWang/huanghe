from __future__ import annotations
from services.cluster.k8s.api.core import Core
from services.cluster.k8s.api.core_v1_api import CoreV1Api
from services.cluster.k8s.model.v1_pod import V1Pod
from services.cluster.pod.serializers import Pod


class PodMixin(CoreV1Api):
    def __init__(self, c: Core):
        super(PodMixin, self).__init__(c=c)

    def list_namespaced_pod(self):
        return self.core_v1_api.list_namespaced_pod()

    def create_namespaced_pod(self, namespace: str, name: str, image: str):
        return self.core_v1_api.create_namespaced_pod(namespace, body=V1Pod.default(name=name,
                                                                                    namespace=namespace,
                                                                                    image=image))

    def read_namespaced_pod_log(self, p: Pod):
        return self.core_v1_api.read_namespaced_pod_log(name=p.name, namespace=p.namespace)
