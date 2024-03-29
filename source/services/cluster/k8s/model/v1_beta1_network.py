from services.cluster.k8s.model.base_model import BaseModel
from services.cluster.k8s.model.v1_beta1_network_spec import V1Beta1NetworkSpec
from services.cluster.k8s.model.v1_object_meta import V1ObjectMeta
from services.cluster.k8s.const.crd_kubeflow_const import HUAWEICLOUD_NETWORK_APIVERSION, HUAWEICLOUD_NETWORK_KIND


class V1Beta1Network(BaseModel):
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
    spec = V1Beta1NetworkSpec

    openapi_types = {
        'api_version': 'str',
        'kind': 'str',
        'metadata': 'V1ObjectMeta',
        'spec': 'V1NetworkSpec',
        # 'status': 'V1IngressStatus'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'kind': 'kind',
        'metadata': 'metadata',
        'spec': 'spec',
        'status': 'status'
    }

    @classmethod
    def default(cls, name: str, namespace: str):
        return cls.new(api_version=HUAWEICLOUD_NETWORK_APIVERSION,
                       kind=HUAWEICLOUD_NETWORK_KIND,
                       metadata=V1ObjectMeta.huaweicloud_network(name=name, namespace=namespace),
                       spec=V1Beta1NetworkSpec.default())

    @staticmethod
    def new(api_version: str, kind: str, metadata: V1ObjectMeta, spec: V1Beta1NetworkSpec):
        return V1Beta1Network(api_version=api_version, kind=kind, metadata=metadata, spec=spec)


if __name__ == '__main__':
    d = V1Beta1Network.default(name="test", namespace="test-ns").dict()
    import pprint
    pprint.pprint(d)