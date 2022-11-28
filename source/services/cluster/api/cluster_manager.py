from api.namespace_mixin import NamespaceMixin
from api.notebook_mixin import NotebookMixin
from api.pod_mixin import PodMixin

class ClusterManager(NamespaceMixin, NotebookMixin, PodMixin):
    pass






if __name__ == '__main__':
    cm = ClusterManager
    from api import c
    cm.create_notebook(c=c, name="jiangshouchen", namespace="default", image="dddssssssss")







