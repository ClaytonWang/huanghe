from __future__ import annotations
from typing import Optional
from k8s.model.generic_mixin import GenericMixin


class V1EmptyDirVolumeSource(GenericMixin):
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
    medium: str
    size_limit: Optional[str]
    openapi_types = {
        'medium': 'str',
        'size_limit': 'str'
    }

    attribute_map = {
        'medium': 'medium',
        'size_limit': 'sizeLimit'
    }

    @classmethod
    def default(cls):
        return cls.new(medium="Memory")

    @staticmethod
    def new(medium: str, size_limit: Optional[str]=None):
        return V1EmptyDirVolumeSource(medium=medium, size_limit=size_limit)
