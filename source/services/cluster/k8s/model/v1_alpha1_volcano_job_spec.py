from __future__ import annotations
from k8s.model.generic_mixin import GenericMixin
from k8s.model.v1_alpha1_volcano_job_task import V1Alpha1VolcanoJobTask
from typing import List, Optional
from k8s.const.crd_kubeflow_const import VOLCANO_DEFAULT_QUEUE, VOLCANO_DEFAULT_MAX_RETRY, VOLCANO_DEFAULT_MIN_AVAILABLE

class V1Alpha1VolcanoJobSpec(GenericMixin):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    min_available: Optional[int]
    scheduler_name: Optional[str]
    priority_class_name: Optional[str]
    policies: Optional[List]
    max_retry: Optional[int]
    queue: Optional[str]
    tasks: List[V1Alpha1VolcanoJobTask]

    openapi_types = {
        "min_available": 'int',
        "scheduler_name": "str",
        "priority_class_name": "str",
        "policies": "str",
        "max_retry": "int",
        "queue": "str",
        "tasks": "List[V1Alpha1VolcanoJobTask]",
    }
    attribute_map = {
        'min_available': 'minAvailable',
        "scheduler_name": "schedulerName",
        'priority_class_name': "priorityClassName",
        "policies": "policies",
        "max_retry": "maxRetry",
        "queue": "queue",
        "tasks": "tasks"
    }

    def set_scheduler(self, scheduler_name):
        self.scheduler_name = scheduler_name
        return self

    def set_queue(self, queue):
        self.queue = queue
        return self

    def set_min_available(self, min_available):
        self.min_available = min_available
        return self

    def set_max_retry(self, max_retry):
        self.max_retry = max_retry
        return self

    @classmethod
    def default(cls, name, image, resource, envs, volumes, tolerations):
        spec = cls.new([V1Alpha1VolcanoJobTask.default(name=name, image=image, resource=resource, envs=envs, volumes=volumes, tolerations=tolerations)])
        spec.set_queue(VOLCANO_DEFAULT_QUEUE).set_max_retry(VOLCANO_DEFAULT_MAX_RETRY).set_min_available(VOLCANO_DEFAULT_MIN_AVAILABLE)
        return spec


    @staticmethod
    def new(tasks: List[V1Alpha1VolcanoJobTask], min_available: Optional[int] = None, scheduler_name: Optional[str] = None,
            priority_class_name: Optional[str] = None, policies: Optional[List] = None, max_retry: Optional[int] = None, queue: Optional[str] = None) -> V1Alpha1VolcanoJobSpec:
        return V1Alpha1VolcanoJobSpec(tasks=tasks, min_available=min_available, scheduler_name=scheduler_name,
                                      priority_class_name=priority_class_name, policies=policies, max_retry=max_retry, queue=queue)
