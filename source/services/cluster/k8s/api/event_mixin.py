import datetime

from services.cluster.event.serializers import Event
from services.cluster.k8s.api.core import K8sConfigFactory
from services.cluster.k8s.api.core_v1_api import CoreV1Api


class EventMixin(CoreV1Api):
    def __init__(self, kcf: K8sConfigFactory):
        super(EventMixin, self).__init__(kcf=kcf)

    def list_event(self, event: Event):
        result = self.core_v1_api(cluster=event.cluster).list_namespaced_event(
            namespace=event.namespace,
            label_selector=",".join([f"{key}={val}" for key, val in event.label_selector.items()]))
        events = []
        for event in result.items:
            metadata = event.metadata
            events.append({
                "message": event.message,
                "namespace": metadata.namespace,
                "event_name": metadata.name,
                "self_link": metadata.self_link,
                "labels": metadata.labels,
                "reason": event.reason,
                "type": event.type,
                "last_timestamp": (event.last_timestamp+datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            })
        return events
