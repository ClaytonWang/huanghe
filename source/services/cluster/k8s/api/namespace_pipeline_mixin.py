from __future__ import annotations
from services.cluster.k8s.api.core import K8sConfigFactory
from services.cluster.k8s.api.namespace_mixin import NamespaceMixin
from services.cluster.k8s.api.network_mixin import NetworkMixin
from services.cluster.k8s.model.v1_status import V1Status
from services.cluster.namespace_pipeline.serializers import NamespacePipeline, Namespace


class NamespacePipelineMixin(NamespaceMixin, NetworkMixin):
    def __init__(self, kcf: K8sConfigFactory):
        super(NamespacePipelineMixin, self).__init__(kcf=kcf)

    def create_namespace_pipeline(self, np: NamespacePipeline):
        self.create_huaweiyun_cpu_ns(np.gen_namespace()) and self.create_network(np.gen_network())
        np.name = np.name + "-" + "gpu"
        self.create_huaweiyun_gpu_ns(np.gen_namespace()) and self.create_network(np.gen_network())

    def delete_namespace_pipeline(self, ns: Namespace):
        self.delete_namespace(ns)
        ns.name = ns.name + "-" + "gpu"
        self.delete_namespace(ns)