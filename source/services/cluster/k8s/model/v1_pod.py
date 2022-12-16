# coding: utf-8
from __future__ import annotations
from k8s.model.base_model import BaseModel
from typing import Optional
from k8s.const.workloads_const import API_VERSION_V1, POD_KIND
from k8s.model.v1_object_meta import V1ObjectMeta
from k8s.model.v1_pod_spec import V1PodSpec
from k8s.model.v1_pod_status import V1PodStatus


class V1Pod(BaseModel):
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
    spec: V1PodSpec
    status: Optional[V1PodStatus]


    openapi_types = {
        'api_version': 'str',
        'kind': 'str',
        'metadata': 'V1ObjectMeta',
        'spec': 'V1PodSpec',
        'status': 'V1PodStatus'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'kind': 'kind',
        'metadata': 'metadata',
        'spec': 'spec',
        'status': 'status'
    }

    @classmethod
    def default(cls, name, namespace, image):
        return cls.new(api_version=API_VERSION_V1, kind=POD_KIND, metadata=V1ObjectMeta.default(name=name,
                                                                                                namespace=namespace),
                       spec=V1PodSpec.default(name=name, image=image), status=None)

    @staticmethod
    def new(api_version: str, kind: str, metadata: V1ObjectMeta, spec: V1PodSpec, status: Optional[V1PodStatus]):
        return V1Pod(api_version=api_version, kind=kind, metadata=metadata, spec=spec, status=status)