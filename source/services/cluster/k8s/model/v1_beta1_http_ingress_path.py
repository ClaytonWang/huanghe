from services.cluster.k8s.model.base_model import GenericMixin
from services.cluster.k8s.model.v1_beta1_ingress_backend import V1Beta1IngressBackend
from typing import Dict, Optional

class V1Beta1HTTPIngressPath(GenericMixin):
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
    backend: V1Beta1IngressBackend
    path: Optional[str]
    property: Optional[Dict[str, str]]

    openapi_types = {
        "backend": "V1Beta1IngressBackend",
        "path": "str",
        "property": "Dict[str, str]"
    }

    attribute_map = {
        'backend': 'backend',
        'path': 'path',
        'property': "property",
    }

    @classmethod
    def default(cls, service_name: str):
        return cls.new(backend=V1Beta1IngressBackend.default(service_name=service_name, service_port="80"))

    @staticmethod
    def new(backend: V1Beta1IngressBackend, path: str = None, property: Dict[str, str] = None):
        return V1Beta1HTTPIngressPath(backend=backend, path=path, property=property)