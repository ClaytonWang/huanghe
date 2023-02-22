from k8s.model.generic_mixin import GenericMixin


class V1Probe(GenericMixin):
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
        '_exec': 'V1ExecAction',
        'failure_threshold': 'int',
        'grpc': 'V1GRPCAction',
        'http_get': 'V1HTTPGetAction',
        'initial_delay_seconds': 'int',
        'period_seconds': 'int',
        'success_threshold': 'int',
        'tcp_socket': 'V1TCPSocketAction',
        'termination_grace_period_seconds': 'int',
        'timeout_seconds': 'int'
    }

    attribute_map = {
        '_exec': 'exec',
        'failure_threshold': 'failureThreshold',
        'grpc': 'grpc',
        'http_get': 'httpGet',
        'initial_delay_seconds': 'initialDelaySeconds',
        'period_seconds': 'periodSeconds',
        'success_threshold': 'successThreshold',
        'tcp_socket': 'tcpSocket',
        'termination_grace_period_seconds': 'terminationGracePeriodSeconds',
        'timeout_seconds': 'timeoutSeconds'
    }
