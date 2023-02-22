from k8s.model.generic_mixin import GenericMixin


class V1Status(GenericMixin):
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
    code: int
    details: str
    kind: str
    message: str
    metadata: str
    reason: str
    status: str

    openapi_types = {
        'api_version': 'str',
        'code': 'int',
        'details': 'V1StatusDetails',
        'kind': 'str',
        'message': 'str',
        'metadata': 'V1ListMeta',
        'reason': 'str',
        'status': 'str'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'code': 'code',
        'details': 'details',
        'kind': 'kind',
        'message': 'message',
        'metadata': 'metadata',
        'reason': 'reason',
        'status': 'status'
    }
