from model.generic_mixin import GenericMixin


class V1EnvFromSource(GenericMixin):
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
        'config_map_ref': 'V1ConfigMapEnvSource',
        'prefix': 'str',
        'secret_ref': 'V1SecretEnvSource'
    }

    attribute_map = {
        'config_map_ref': 'configMapRef',
        'prefix': 'prefix',
        'secret_ref': 'secretRef'
    }