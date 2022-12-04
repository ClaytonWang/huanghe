from kubernetes.client import V1PodDNSConfig

class V1PodDNSConfig(object):
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
        'nameservers': 'list[str]',
        'options': 'list[V1PodDNSConfigOption]',
        'searches': 'list[str]'
    }

    attribute_map = {
        'nameservers': 'nameservers',
        'options': 'options',
        'searches': 'searches'
    }