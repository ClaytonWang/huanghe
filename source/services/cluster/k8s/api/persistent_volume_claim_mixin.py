from __future__ import annotations
from k8s.api.core import Core
from k8s.api.core_v1_api import CoreV1Api
from k8s.model.v1_persistent_volume_claim import V1PersistentVolumeClaim
from k8s.model.v1_status import V1Status
from pvc.serializers import PVCCreateReq, PVCDeleteReq
from basic.config.cluster import VOLUME_STORAGE_CLASS_JUICEFS

class PersistentVolumeClaimMixin(CoreV1Api):
    def __init__(self, c: Core):
        super(PersistentVolumeClaimMixin, self).__init__(c=c)

    def create_namespaced_persistent_volume_claim(self, pvc: PVCCreateReq) -> V1PersistentVolumeClaim:
        return self.core_v1_api.create_namespaced_persistent_volume_claim(namespace=pvc.namespace,
                                                                          body=V1PersistentVolumeClaim.default(name=pvc.name,
                                                                                                               namespace=pvc.namespace,
                                                                                                               size=pvc.size,
                                                                                                               env=pvc.env,
                                                                                                               platform=pvc.platform,
                                                                                                               sc=VOLUME_STORAGE_CLASS_JUICEFS))

    def delete_namespaced_persistent_volume_claim(self, pdr: PVCDeleteReq) -> V1Status:
        return self.core_v1_api.delete_namespaced_persistent_volume_claim(name=pdr.name,
                                                                          namespace=pdr.namespace)

