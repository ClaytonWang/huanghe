from services.cluster.k8s.model.base_model import GenericMixin
from services.cluster.k8s.model.v1_beta1_ingress_rule import V1Beta1IngressRule
from services.cluster.k8s.model.v1_beta1_ingress_tls import V1Beta1IngressTLS
from services.cluster.k8s.model.v1_beta1_ingress_backend import V1Beta1IngressBackend
from typing import List, Optional

class V1Beta1IngressSpec(GenericMixin):
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

    backend: Optional[V1Beta1IngressBackend]
    rules: Optional[List[V1Beta1IngressRule]]
    tls: Optional[List[V1Beta1IngressTLS]]

    openapi_types = {
        'backend': 'V1Beta1Backend',
        'rules': 'V1Beta1IngressRule',
        'tls': 'V1Beta1IngressTLS',
    }

    attribute_map = {
        'backend': 'backend',
        'rules': 'rules',
        'tls': "tls",
    }


    @classmethod
    def default(cls, service_name):
        return cls.new(rules=[V1Beta1IngressRule.default(service_name=service_name)],)

    @staticmethod
    def new(rules: List[V1Beta1IngressRule], tls: List[V1Beta1IngressTLS] = None, backend: V1Beta1IngressBackend=None):
        return V1Beta1IngressSpec(backend=backend, rules=rules, tls=tls)