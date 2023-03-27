from services.cluster.k8s.api.event_mixin import EventMixin
from services.cluster.k8s.api.namespace_mixin import NamespaceMixin
from services.cluster.k8s.api.notebook_mixin import NotebookMixin
from services.cluster.k8s.api.pod_mixin import PodMixin
from services.cluster.k8s.api.persistent_volume_claim_mixin import PersistentVolumeClaimMixin
from services.cluster.k8s.api.secret_mixin import SecretMixin
from services.cluster.k8s.api.volcano_job_mixin import VolcanoJobMixin
from services.cluster.k8s.api.server_mixin import ServerMixin
from services.cluster.k8s.api.deployment_mixin import DeploymentMixin
from services.cluster.k8s.api.service_mixin import ServiceMixin
from services.cluster.k8s.api import c, hw


class ClusterClient(NamespaceMixin, NotebookMixin, PodMixin, PersistentVolumeClaimMixin,
                    SecretMixin, VolcanoJobMixin, ServerMixin, DeploymentMixin, ServiceMixin, EventMixin):

    def __init__(self, cluster_name=None):
        if cluster_name == 'huawei':
            super(ClusterClient, self).__init__(c=hw)
        else:
            super(ClusterClient, self).__init__(c=c)


cc = ClusterClient()
hwc = ClusterClient(cluster_name='huawei')

if __name__ == '__main__':
    pass
