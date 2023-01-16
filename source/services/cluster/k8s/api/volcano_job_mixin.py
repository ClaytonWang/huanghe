from __future__ import annotations
from k8s.api.core import Core
from k8s.model.v1_status import V1Status
from k8s.api.custom_object_api import CustomerObjectApi
from k8s.api.core_v1_api import CoreV1Api
from k8s.const.crd_kubeflow_const import VOLCANO_JOB_GROUP, VOLCANO_JOB_PLURAL, VOLCANO_V1_ALPHA1_VERSION
from k8s.model.v1_alpha1_volcano_job import V1Alpha1VolcanoJob
from volcanojob.serializers import VolcanoJob, VolcanoJobDeleteReq
from typing import Optional, Dict



class VolcanoJobMixin(CustomerObjectApi, CoreV1Api):
    def __init__(self, c: Core):
        super(VolcanoJobMixin, self).__init__(c=c)

    def create_vcjob(self, vj: VolcanoJob) -> Dict:
        return self.custom_object_api.create_namespaced_custom_object(group=VOLCANO_JOB_GROUP,
                                                                      version=VOLCANO_V1_ALPHA1_VERSION,
                                                                      namespace=vj.namespace,
                                                                      plural=VOLCANO_JOB_PLURAL,
                                                                      body=V1Alpha1VolcanoJob.default(name=vj.name,
                                                                                                      namespace=vj.namespace,
                                                                                                      image=vj.image,
                                                                                                      labels=vj.labels,
                                                                                                      resource=vj.resource,
                                                                                                      envs=vj.envs,
                                                                                                      volumes=vj.volumes,
                                                                                                      tolerations=vj.tolerations,
                                                                                                      ),
                                                                      )


    def delete_vcjob(self, vjdr: VolcanoJobDeleteReq) -> V1Status:
        return self.custom_object_api.delete_namespaced_custom_object(group=VOLCANO_JOB_GROUP,
                                                                      version=VOLCANO_V1_ALPHA1_VERSION,
                                                                      namespace=vjdr.namespace,
                                                                      plural=VOLCANO_JOB_PLURAL,
                                                                      name=vjdr.name)


    def list_volcanojob(self, vjdr: VolcanoJobDeleteReq):
        volcanojob = []

        for volcanojob in self.custom_object_api.list_cluster_custom_object(group=VOLCANO_JOB_GROUP,
                                                                            version=VOLCANO_V1_ALPHA1_VERSION,
                                                                            plural=VOLCANO_JOB_PLURAL,
                                                                            label_selector=f"env={vjdr.env}"
                                                                            )['items']:
            volcanojob_name = volcanojob["metadata"]["name"]
            volcanojob.append(volcanojob_name)

        return volcanojob


