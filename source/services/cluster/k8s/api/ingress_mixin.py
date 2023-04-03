from __future__ import annotations
from services.cluster.k8s.api.core import K8sConfigFactory
from services.cluster.k8s.api.v1_beta1_api import V1Beta1Api
from services.cluster.k8s.model.v1_beta1_ingress import V1Beta1Ingress
from services.cluster.ingress.serializers import Ingress
import random


class IngressMixin(V1Beta1Api):
    def __init__(self, kcf: K8sConfigFactory):
        super(IngressMixin, self).__init__(kcf=kcf)

    def create_ingress(self, ig: Ingress) -> V1Beta1Ingress:
        return self.v1_beta1_api(cluster=ig.cluster).create_namespaced_ingress(namespace=ig.namespace,
               body=V1Beta1Ingress.default(name=ig.name, namespace=ig.namespace, port=str(self.random_port())))

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


    @staticmethod
    def random_port():
        return random.randint(5000, 65500)