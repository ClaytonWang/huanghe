from __future__ import annotations
from core import Core

class PodMixin():
    def list_namespaced_pod(self):
        return self.c.core_v1_api.list_namespaced_pod()
