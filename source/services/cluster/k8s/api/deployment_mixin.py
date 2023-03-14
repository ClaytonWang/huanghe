from __future__ import annotations
from services.cluster.k8s.api.core import Core
from services.cluster.k8s.model.v1_status import V1Status
from services.cluster.k8s.api.apps_v1_api import AppsV1Api
from services.cluster.k8s.model.v1_deployment import V1Deployment
from services.cluster.deployment.serializers import Deployment, DeploymentDeleteReq, DeploymentListReq
from typing import Dict


class DeploymentMixin(AppsV1Api):
    def __init__(self, c: Core):
        super(DeploymentMixin, self).__init__(c=c)

    def create_deployment(self, d: Deployment) -> Dict:
        return self.apps_v1_api.create_namespaced_deployment(namespace=d.namespace,
                                                             body=V1Deployment.default(name=d.name,
                                                                                       namespace=d.namespace,
                                                                                       image=d.image,
                                                                                       labels=d.labels))

    def delete_deployment(self, ddr: DeploymentDeleteReq) -> V1Status:
        return self.apps_v1_api.delete_namespaced_deployment(name=ddr.name,
                                                             namespace=ddr.namespace)

    def list_deployment(self, dlr: DeploymentListReq):
        return self.apps_v1_api.list_namespaced_deployment(namespace=dlr.namespace)
