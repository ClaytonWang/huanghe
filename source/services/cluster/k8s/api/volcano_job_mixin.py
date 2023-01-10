from __future__ import annotations
from k8s.api.core import Core
from k8s.model.v1_status import V1Status
from k8s.api.custom_object_api import CustomerObjectApi
from k8s.api.core_v1_api import CoreV1Api
from k8s.const.crd_kubeflow_const import VOLCANO_JOB_GROUP, VOLCANO_JOB_KIND, VOLCANO_JOB_PLURAL, VOLCANO_V1_ALPHA1_API_VERSION, VOLCANO_V1_ALPHA1_VERSION
from k8s.model.v1_alpha1_volcano_job import V1Alpha1VolcanoJob
from volcanojob.serializers import VolcanoJob
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

    # def delete_notebook(self, nbdr: NoteBookDeleteReq) -> V1Status:
    #     return self.custom_object_api.delete_namespaced_custom_object(group=KUBEFLOW_NOTEBOOK_GROUP,
    #                                                                   version=KUBEFLOW_V1_VERSION,
    #                                                                   namespace=nbdr.namespace,
    #                                                                   plural=KUBEFLOW_NOTEBOOK_PLURAL,
    #                                                                   name=nbdr.name,)
    #
    # def list_notebook(self, nblr: NoteBookListReq):
    #     notebooks = []
    #
    #     for notebook in self.custom_object_api.list_cluster_custom_object(group=KUBEFLOW_NOTEBOOK_GROUP,
    #                                                                       version=KUBEFLOW_V1_VERSION,
    #                                                                       plural=KUBEFLOW_NOTEBOOK_PLURAL,
    #                                                                       label_selector=f"env={nblr.env}"
    #                                                                       )['items']:
    #         notebook_name = notebook["metadata"]['name']
    #         namespace = notebook["metadata"]['namespace']
    #         status = NOTEBOOK_STATUS_ON if self.is_ready(notebook) else NOTEBOOK_STATUS_PENDING
    #         if NOTEBOOK_STATUS_ON == status:
    #             status, reason = NOTEBOOK_STATUS_ON, "success"
    #         else:
    #             status, reason = self.process_notebook_status(notebook_name, namespace)
    #         notebooks.append({"name": notebook_name,
    #                           "namespace": namespace,
    #                           "status": status,
    #                           "reason": reason,
    #                           "url": f"https://kubeflow.digitalbrain.cn:31443/notebook/{namespace}/{notebook_name}/lab"})
    #     return notebooks
