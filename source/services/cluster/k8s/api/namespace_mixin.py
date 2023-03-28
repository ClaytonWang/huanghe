from __future__ import annotations
from services.cluster.k8s.api.core import K8sConfigFactory
from services.cluster.k8s.api.core_v1_api import CoreV1Api
from services.cluster.k8s.model.v1_namespace import V1Namespace
from services.cluster.k8s.model.v1_status import V1Status
from services.cluster.namespace.serializers import Namespace


class NamespaceMixin(CoreV1Api):
    def __init__(self, kcf: K8sConfigFactory):
        super(NamespaceMixin, self).__init__(kcf=kcf)

    def create_namespace(self, ns: Namespace) -> V1Namespace:
        return self.core_v1_api(cluster=ns.cluster).create_namespace(body=V1Namespace.default(name=ns.name, labels=ns.labels))

    def delete_namespace(self, ns: Namespace) -> V1Status:
        return self.core_v1_api(cluster=ns.cluster).delete_namespace(name=ns.name)
    #
    def create_huaweiyun_gpu_ns(self, ns: Namespace):
        return self.core_v1_api(cluster=ns.cluster).create_namespace(body=V1Namespace.huaweicloud_gpu(name=ns.name,
                                                                                  labels=ns.labels))

    def create_huaweiyun_cpu_ns(self, ns: Namespace):
        return self.core_v1_api(cluster=ns.cluster).create_namespace(body=V1Namespace.huaweicloud_cpu(name=ns.name,
                                                                                  labels=ns.labels))