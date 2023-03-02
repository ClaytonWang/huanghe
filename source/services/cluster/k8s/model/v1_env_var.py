from __future__ import annotations
from services.cluster.k8s.model.generic_mixin import GenericMixin


class V1EnvVar(GenericMixin):
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
    value: str
    openapi_types = {
        'name': 'str',
        'value': 'str',
        # 'value_from': 'V1EnvVarSource'
    }

    attribute_map = {
        'name': 'name',
        'value': 'value',
        # 'value_from': 'valueFrom'
    }

    @staticmethod
    def new(name: str, value: str):
        return V1EnvVar(name=name, value=value)
