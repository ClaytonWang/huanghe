from services.cluster.k8s.api.namespace_mixin import NamespaceMixin
from services.cluster.k8s.api.notebook_mixin import NotebookMixin
from services.cluster.k8s.api.pod_mixin import PodMixin
from services.cluster.k8s.api.persistent_volume_claim_mixin import PersistentVolumeClaimMixin
from services.cluster.k8s.api.secret_mixin import SecretMixin
from services.cluster.k8s.api.volcano_job_mixin import VolcanoJobMixin
from services.cluster.k8s.api.server_mixin import ServerMixin
from services.cluster.k8s.api import c


class ClusterClient(NamespaceMixin, NotebookMixin, PodMixin, PersistentVolumeClaimMixin,
                    SecretMixin, VolcanoJobMixin, ServerMixin):

    def __init__(self):
        super(ClusterClient, self).__init__(c=c)


cc = ClusterClient()

if __name__ == '__main__':
    pass
