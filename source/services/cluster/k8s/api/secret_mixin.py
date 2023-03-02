from __future__ import annotations
from services.cluster.k8s.api.core import Core
from services.cluster.k8s.api.core_v1_api import CoreV1Api
from services.cluster.k8s.model.v1_secret import V1Secret
from services.cluster.k8s.model.v1_status import V1Status
from secret.serializers import SecretCommon, SecretNamespace


class SecretMixin(CoreV1Api):
    def __init__(self, c: Core):
        super(SecretMixin, self).__init__(c=c)

    def create_namespaced_secret(self, sn: SecretNamespace) -> V1Secret:
        return self.core_v1_api.create_namespaced_secret(namespace=sn.namespace,
                                                         body=V1Secret.huaweiyun_swr_secret(namespace=sn.namespace))

    def read_namespaced_secret(self, sc: SecretCommon) -> V1Secret:
        return self.core_v1_api.read_namespaced_secret(name=sc.name,
                                                       namespace=sc.namespace)

    def delete_namespaced_secret(self, sc: SecretCommon) -> V1Status:
        return self.core_v1_api.delete_namespaced_secret(name=sc.name, namespace=sc.namespace)
