from services.cluster.k8s.api.service_mixin import ServiceMixin
from services.cluster.k8s.api.deployment_mixin import DeploymentMixin
from services.cluster.k8s.api.ingress_mixin import IngressMixin
from services.cluster.service_pipeline.serializers import ServicePipeline, ServicePipelineDeleteReq
from services.cluster.k8s.api.core import K8sConfigFactory
from typing import Dict

class ServicePipelineMixin(DeploymentMixin, ServiceMixin, IngressMixin):
    def __init__(self, kcf: K8sConfigFactory):
        super(ServiceMixin, self).__init__(kcf=kcf)

    def create_service_pipeline(self, sp: ServicePipeline) -> Dict:
        return self.create_deployment(sp.gen_deployment()) and self.create_service(sp.gen_service()) and self.create_ingress(sp.gen_ingress())

    def delete_service_pipeline(self, sp: ServicePipelineDeleteReq):
        pass
        # return self.delete



