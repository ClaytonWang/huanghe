# coding: utf-8
from __future__ import annotations
from k8s.model.generic_mixin import GenericMixin
from typing import Optional, Dict
from k8s.const.workloads_const import API_VERSION_V1, SECRET_KIND, \
    SECRET_TYPE_DOCKER_CONFIG, SECRET_DATA_DOCKER_CONFIG, SECRET_NAME_DOCKER_CONFIG
from k8s.model.v1_object_meta import V1ObjectMeta


class V1Secret(GenericMixin):
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
    api_version: str
    data: Dict[str, str]
    immutable: Optional[bool]
    kind: str
    metadata: Optional[V1ObjectMeta]
    string_data: Optional[Dict[str, str]]
    type: str
    openapi_types = {
        'api_version': 'str',
        'data': 'dict(str, str)',
        'immutable': 'bool',
        'kind': 'str',
        'metadata': 'V1ObjectMeta',
        'string_data': 'dict(str, str)',
        'type': 'str'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'data': 'data',
        'immutable': 'immutable',
        'kind': 'kind',
        'metadata': 'metadata',
        'string_data': 'stringData',
        'type': 'type'
    }

    @classmethod
    def default(cls, name, namespace, data, type):
        return cls.new(api_version=API_VERSION_V1, kind=SECRET_KIND, metadata=V1ObjectMeta.default(name=name, namespace=namespace)
                       ,data=data, type=type)

    @classmethod
    def huaweiyun_swr_secret(cls, namespace):
        return cls.default(name=SECRET_NAME_DOCKER_CONFIG, namespace=namespace, data=SECRET_DATA_DOCKER_CONFIG, type=SECRET_TYPE_DOCKER_CONFIG)

    @staticmethod
    def new(api_version: str, data: Dict[str, str],
            kind: str, metadata: V1ObjectMeta, type, string_data = None, immutable: Optional[bool] = None):
        return V1Secret(api_version=api_version, data=data, immutable=immutable,
                        kind=kind, metadata=metadata, string_data=string_data, type=type)