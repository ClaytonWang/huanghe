# coding: utf-8
from __future__ import annotations
from services.cluster.k8s.model.base_model import BaseModel
from services.cluster.k8s.model.v1_namespace_spec import V1NamespaceSpec
from services.cluster.k8s.model.v1_namespace_status import V1NamespaceStatus
from services.cluster.k8s.model.v1_object_meta import V1ObjectMeta
from services.cluster.k8s.const.workloads_const import API_VERSION_V1, NAMESPACE_KIND
from typing import Optional


class V1Namespace(BaseModel):
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
    spec: V1NamespaceSpec
    status: Optional[V1Namespace]
    openapi_types: dict = {
        'api_version': 'str',
        'kind': 'str',
        'metadata': 'V1ObjectMeta',
        'spec': 'V1NamespaceSpec',
        'status': 'V1NamespaceStatus'
    }
    attribute_map: dict = {
        'api_version': 'apiVersion',
        'kind': 'kind',
        'metadata': 'metadata',
        'spec': 'spec',
        'status': 'status'
    }

    @classmethod
    def default(cls, name: str, labels):
        return cls.new(api_version=API_VERSION_V1, kind=NAMESPACE_KIND,
                       metadata=V1ObjectMeta.default(name=name, labels=labels), spec=V1NamespaceSpec.new(None),
                       status=None)

    @classmethod
    def huaweicloud_gpu(cls, name: str, labels):
        return cls.new(api_version=API_VERSION_V1,
                       kind=NAMESPACE_KIND,
                       metadata=V1ObjectMeta.huaweicloud_gpu_namespace(name=name, labels=labels),
                       spec=V1NamespaceSpec.new(None),
                       status=None)

    @classmethod
    def huaweicloud_cpu(cls, name: str, labels):
        return cls.new(api_version=API_VERSION_V1,
                       kind=NAMESPACE_KIND,
                       metadata=V1ObjectMeta.huaweicloud_cpu_namespace(name=name, labels=labels),
                       spec=V1NamespaceSpec.new(None),
                       status=None)

    @staticmethod
    def new(api_version: str, kind: str, metadata: V1ObjectMeta, spec: V1NamespaceSpec,
            status: Optional[V1NamespaceStatus]):
        return V1Namespace(api_version=api_version, kind=kind, metadata=metadata, spec=spec, status=status)
