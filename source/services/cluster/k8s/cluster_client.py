from k8s.api.namespace_mixin import NamespaceMixin
from k8s.api.notebook_mixin import NotebookMixin
from k8s.api.pod_mixin import PodMixin
from k8s.api import c


class ClusterClient(NamespaceMixin, NotebookMixin, PodMixin):

    def __init__(self):
        super(ClusterClient, self).__init__(c=c)







cc = ClusterClient()

if __name__ == '__main__':
    print(cc.create_namespace("sssss"))






