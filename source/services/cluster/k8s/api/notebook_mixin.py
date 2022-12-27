from __future__ import annotations
from k8s.api.core import Core
from k8s.model.v1_status import V1Status
from k8s.api.custom_object_api import CustomerObjectApi
from k8s.const.crd_kubeflow_const import KUBEFLOW_NOTEBOOK_GROUP, KUBEFLOW_V1_VERSION, KUBEFLOW_NOTEBOOK_PLURAL
from k8s.model.v1_notebook import V1Notebook
from typing import Optional, Dict
from notebook.serializers import NoteBook, NoteBookListReq, NoteBookDeleteReq

class NotebookMixin(CustomerObjectApi):
    def __init__(self, c: Core):
        super(NotebookMixin, self).__init__(c=c)


    def create_notebook(self, nb: NoteBook) -> Dict:
        return self.custom_object_api.create_namespaced_custom_object(group=KUBEFLOW_NOTEBOOK_GROUP,
                                                                        version=KUBEFLOW_V1_VERSION,
                                                                        namespace=nb.namespace,
                                                                        plural=KUBEFLOW_NOTEBOOK_PLURAL,
                                                                        body=V1Notebook.default(name=nb.name,
                                                                                                namespace=nb.namespace,
                                                                                                image=nb.image,
                                                                                                labels=nb.labels,
                                                                                                resource=nb.resource,
                                                                                                envs=nb.envs,
                                                                                                volumes=nb.volumes,
                                                                                                tolerations=nb.tolerations,
                                                                                                ),
                                                                        )


    def delete_notebook(self, nbdr: NoteBookDeleteReq) -> V1Status:
        return self.custom_object_api.delete_namespaced_custom_object(name=nbdr.name, namespace=nbdr.namespace)

    def list_notebook(self, nblr: NoteBookListReq):
        return self.custom_object_api.list_cluster_custom_object(group=KUBEFLOW_NOTEBOOK_GROUP,
                                                                 version=KUBEFLOW_V1_VERSION,
                                                                 plural=KUBEFLOW_NOTEBOOK_PLURAL,
                                                                 label_selector=f"env={nblr.env}"
                                                                    )

    def watch_notebook(self):
        return self.custom_object_api.list_namespaced_custom_object