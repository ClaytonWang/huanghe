from __future__ import annotations
from k8s.model.generic_mixin import GenericMixin

class V1Lifecycle(GenericMixin):
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
    openapi_types = {
        'post_start': 'V1LifecycleHandler',
        'pre_stop': 'V1LifecycleHandler'
    }

    attribute_map = {
        'post_start': 'postStart',
        'pre_stop': 'preStop'
    }