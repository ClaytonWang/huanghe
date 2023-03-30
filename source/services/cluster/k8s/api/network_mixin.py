from __future__ import annotations
from services.cluster.k8s.api.core import K8sConfigFactory
from services.cluster.k8s.api.v1_beta1_api import V1Beta1Api
from services.cluster.k8s.model.v1_beta1_network import V1Beta1Network
from services.cluster.network.serializers import Network


class NetworkMixin(V1Beta1Api):
    def __init__(self, kcf: K8sConfigFactory):
        super(NetworkMixin, self).__init__(kcf=kcf)

    def create_network(self, nw: Network) -> V1Beta1Network:
        return self.v1_beta1_api(cluster=nw.cluster).create_namespaced_network(namespace=nw.namespace,
               body=V1Beta1Network.default(name=nw.name, namespace=nw.namespace))

    # def delete_namespace(self, ns: Namespace) -> V1Status:
    #     return self.core_v1_api(cluster=ns.cluster).delete_namespace(name=ns.name)
    # #
    # def create_huaweiyun_gpu_ns(self, ns: Namespace):
    #     return self.core_v1_api(cluster=ns.cluster).create_namespace(body=V1Namespace.huaweicloud_gpu(name=ns.name,
    #                                                                               labels=ns.labels))
    #
    # def create_huaweiyun_cpu_ns(self, ns: Namespace):
    #     return self.core_v1_api(cluster=ns.cluster).create_namespace(body=V1Namespace.huaweicloud_cpu(name=ns.name,
    #                                                                               labels=ns.labels))