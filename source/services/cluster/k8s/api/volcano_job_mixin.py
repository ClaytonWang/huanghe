from __future__ import annotations
from services.cluster.k8s.api.core import K8sConfigFactory
from services.cluster.k8s.model.v1_status import V1Status
from services.cluster.k8s.api.custom_object_api import CustomerObjectApi
from services.cluster.k8s.api.core_v1_api import CoreV1Api
from services.cluster.k8s.const.crd_kubeflow_const import VOLCANO_JOB_GROUP, VOLCANO_JOB_PLURAL, \
    VOLCANO_V1_ALPHA1_VERSION
from services.cluster.k8s.model.v1_alpha1_volcano_job import V1Alpha1VolcanoJob
from services.cluster.volcanojob.serializers import VolcanoJob, VolcanoJobDeleteReq, VolcanoJobListReq
from typing import Dict


class VolcanoJobMixin(CustomerObjectApi, CoreV1Api):
    def __init__(self, kcf: K8sConfigFactory):
        super(VolcanoJobMixin, self).__init__(kcf=kcf)

    def create_vcjob(self, vj: VolcanoJob) -> Dict:
        return self.custom_object_api(cluster=vj.cluster).create_namespaced_custom_object(group=VOLCANO_JOB_GROUP,
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
                                                                                                      command=vj.command,
                                                                                                      working_dir=vj.working_dir,
                                                                                                      annotations=vj.annotations,
                                                                                                      task_num=vj.task_num,
                                                                                                      mode=vj.mode
                                                                                                      ),
                                                                      )

    def delete_vcjob(self, vjdr: VolcanoJobDeleteReq) -> V1Status:
        return self.custom_object_api(cluster=vjdr.cluster).delete_namespaced_custom_object(group=VOLCANO_JOB_GROUP,
                                                                      version=VOLCANO_V1_ALPHA1_VERSION,
                                                                      namespace=vjdr.namespace,
                                                                      plural=VOLCANO_JOB_PLURAL,
                                                                      name=vjdr.name)

    def list_volcanojob(self, vjdr: VolcanoJobListReq):
        pass
