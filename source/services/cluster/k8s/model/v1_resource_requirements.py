from typing import Dict
from k8s.model.generic_mixin import GenericMixin
from k8s.const.workloads_const import RESOURCE_REQUIREMENTS_ATTRIBUTE_SETS

class V1ResourceRequirements(GenericMixin):
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
    limits: Dict[str, str]
    requests: Dict[str, str]

    openapi_types = {
        'limits': 'dict(str, str)',
        'requests': 'dict(str, str)'
    }

    attribute_map = {
        'limits': 'limits',
        'requests': 'requests'
    }

    @classmethod
    def default(cls, requirements: Dict[str, str]):
        require = {k: v for k, v in requirements.items() if k in RESOURCE_REQUIREMENTS_ATTRIBUTE_SETS}
        return cls.new(limits=require, requests=require)

    @staticmethod
    def new(limits: Dict[str, str], requests: Dict[str, str]):
        return V1ResourceRequirements(limits=limits, requests=requests)