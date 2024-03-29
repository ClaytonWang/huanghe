from services.cluster.k8s.model.generic_mixin import GenericMixin


class V1NodeSelector(GenericMixin):
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
        'node_selector_terms': 'list[V1NodeSelectorTerm]'
    }

    attribute_map = {
        'node_selector_terms': 'nodeSelectorTerms'
    }
