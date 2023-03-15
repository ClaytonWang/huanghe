from __future__ import annotations
from services.cluster.k8s.model.generic_mixin import GenericMixin
from services.cluster.k8s.model.v1_alpha1_volcano_job_task_template import V1Alpha1VolcanoJobTaskTemplate
from services.cluster.k8s.const.crd_kubeflow_const import VOLCANO_TASK_DEFAULT_NAME, VOLCANO_TASK_REPLICAS


class V1Alpha1VolcanoJobTask(GenericMixin):
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
    name: str
    replicas: int = 1
    template: V1Alpha1VolcanoJobTaskTemplate
    openapi_types = {
        'name': 'str',
        'replicas': "int",
        "template": "V1Alpha1VolcanoJobTaskTemplate"
    }

    attribute_map = {
        'name': 'name',
        "replicas": "replicas",
        "template": "template",
    }

    @classmethod
    def default(cls, name, image, resource, envs, volumes, tolerations, command, working_dir, task_num):
        return cls.new(
            template=V1Alpha1VolcanoJobTaskTemplate.default(name=name,
                                                            image=image,
                                                            resource=resource,
                                                            envs=envs,
                                                            volumes=volumes,
                                                            tolerations=tolerations,
                                                            command=command,
                                                            working_dir=working_dir),
            replicas=task_num)

    @staticmethod
    def new(template, name: str = VOLCANO_TASK_DEFAULT_NAME, replicas: int = VOLCANO_TASK_REPLICAS):
        return V1Alpha1VolcanoJobTask(name=name, replicas=replicas, template=template)
