from __future__ import annotations

from typing import List

from services.cluster.k8s.api.core import Core
from services.cluster.k8s.model.v1_status import V1Status
from services.cluster.k8s.api.custom_object_api import CustomerObjectApi
from services.cluster.k8s.api.core_v1_api import CoreV1Api
from services.cluster.k8s.const.crd_kubeflow_const import KUBEFLOW_NOTEBOOK_GROUP, KUBEFLOW_V1_VERSION, KUBEFLOW_NOTEBOOK_PLURAL
from services.cluster.k8s.model.v1_notebook import V1Notebook
from typing import Dict
from notebook.serializers import NoteBook, NoteBookListReq, NoteBookDeleteReq
from basic.config.cluster import KUBEFLOW_NOTEBOOK_URL

NOTEBOOK_STATUS_RUNNING = "RUNNING"
NOTEBOOK_STATUS_PENDING = "PENDING"
NOTEBOOK_STATUS_ERROR = "ERROR"
NOTEBOOK_STATUS_WAITING = "WAITING"
NOTEBOOK_STATUS_ON = "ON"


class NotebookMixin(CustomerObjectApi, CoreV1Api):
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
                                                                                              annotations=nb.annotations,
                                                                                              ),
                                                                      )

    def delete_notebook(self, nbdr: NoteBookDeleteReq) -> V1Status:
        return self.custom_object_api.delete_namespaced_custom_object(group=KUBEFLOW_NOTEBOOK_GROUP,
                                                                      version=KUBEFLOW_V1_VERSION,
                                                                      namespace=nbdr.namespace,
                                                                      plural=KUBEFLOW_NOTEBOOK_PLURAL,
                                                                      name=nbdr.name,)

    def list_notebook(self, nblr: NoteBookListReq) -> List:
        notebooks = []
        for notebook in self.custom_object_api.list_cluster_custom_object(group=KUBEFLOW_NOTEBOOK_GROUP,
                                                                          version=KUBEFLOW_V1_VERSION,
                                                                          plural=KUBEFLOW_NOTEBOOK_PLURAL,
                                                                          label_selector=f"env={nblr.env}"
                                                                          )['items']:
            notebook_name = notebook["metadata"]['name']
            namespace = notebook["metadata"]['namespace']
            status = NOTEBOOK_STATUS_ON if self.is_ready(notebook) else NOTEBOOK_STATUS_PENDING
            if NOTEBOOK_STATUS_ON == status:
                status, reason = NOTEBOOK_STATUS_ON, "success"
            else:
                status, reason = self.process_notebook_status(notebook_name, namespace)
            node_name = "default"
            node_ip = "default"
            notebooks.append({"name": notebook_name,
                              "namespace": namespace,
                              "status": status,
                              "reason": reason,
                              "url": f"{KUBEFLOW_NOTEBOOK_URL}/{namespace}/{notebook_name}/" if "annotations" in notebook['metadata'] and "notebooks.kubeflow.org/http-rewrite-uri" in notebook["metadata"]["annotations"] else f"{KUBEFLOW_NOTEBOOK_URL}/{namespace}/{notebook_name}/lab",
                              "server_ip": node_name,
                              "host_ip": node_ip
                              })
        node_names = {}
        node_ips = {}
        pod_ips = {}
        for pod in self.core_v1_api.list_pod_for_all_namespaces(label_selector=f"env={nblr.env}").items:
            node_names[pod.spec.containers[0].name] = pod.spec.node_name
            node_ips[pod.spec.containers[0].name] = pod.status.host_ip
            pod_ips[pod.spec.containers[0].name] = pod.status.pod_ip
        for notebook in notebooks:
            notebook["server_ip"] = node_names.get(notebook["name"])
            notebook["host_ip"] = node_ips.get(notebook["name"])
            notebook["pod_ip"] = pod_ips.get(notebook["name"])
        return notebooks

    def watch_notebook(self):
        return self.custom_object_api.list_namespaced_custom_object

    @staticmethod
    def is_ready(notebook: Dict):
        if 'status' in notebook and 'readyReplicas' in notebook['status'] and notebook['status']['readyReplicas'] == 1:
            return True
        return False

    def process_notebook_status(self, name, namespace):
        try:
            pod = self.core_v1_api.read_namespaced_pod("{}-0".format(name), namespace)
            # check init-container
            for init_container in pod.status.init_container_statuses:
                # check is finished
                if init_container.state.terminated.exit_code == 0:
                    break
                if init_container.state.running:
                    return NOTEBOOK_STATUS_RUNNING, "init container running"
                if init_container.state.waiting:
                    return NOTEBOOK_STATUS_RUNNING, "init container waiting"
                return NOTEBOOK_STATUS_ERROR, "init container unknow"
                # only main container
            for container in pod.status.container_statuses:
                if container.name == name:
                    if container.state.running:
                        return NOTEBOOK_STATUS_ON, "success"
                    # abnormal exited
                    if container.state.terminated.exit_code and container.state.terminated.exit_code != 0:
                        return NOTEBOOK_STATUS_ERROR, "container exit code not zero"
                    # failed to pull image
                    if container.state.waiting.reason == "ImagePullBackOff":
                        return NOTEBOOK_STATUS_ERROR, "image pull failed"
        except Exception as e:
            return self.process_notebook_event_status(name, namespace)

    def process_notebook_event_status(self, name, namespace):
        nb_events = self.list_notebook_events(name, namespace).items
        if not nb_events:
            return NOTEBOOK_STATUS_PENDING, "without event"
        event = nb_events[-1]
        # when pvc not found
        if event.reason == "BackOff" and 'Back-off pulling image' in event.message:
            return NOTEBOOK_STATUS_ERROR, f"failed to pull image"
        if event.reason == "FailedScheduling" and 'not found' in event.message:
            return NOTEBOOK_STATUS_ERROR, f"failed to scheduler because : {event.message}"
        # when request resource not satisfied
        if event.reason == "FailedScheduling" and 'available' in event.message:
            return NOTEBOOK_STATUS_PENDING, f"not enough resource {event.message}"
        # when readiness\liveiness agent requetst or create or pulling image
        if (event.reason == "Unhealthy" and 'probe failed' in event.message) or event.reason in {"Scheduled",
                                                                                                 "Started",
                                                                                                 "Created",
                                                                                                 "Pulling",
                                                                                                 "Pulled",
                                                                                                 "SuccessfulAttachVolume"}:
            return NOTEBOOK_STATUS_RUNNING, "now is waiting for pod"
        return NOTEBOOK_STATUS_ERROR, "unknow error"

    def list_notebook_events(self, name, namespace):
        return self.core_v1_api.list_namespaced_event(namespace=namespace,
                                                      field_selector="involvedObject.name={}-0".format(name))
