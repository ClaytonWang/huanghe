from __future__ import annotations
from services.cluster.k8s.model.base_model import BaseModel
from services.cluster.k8s.model.v1_persistent_volume_claim_spec import V1PersistentVolumeClaimSpec
from services.cluster.k8s.model.v1_object_meta import V1ObjectMeta
from services.cluster.k8s.const.workloads_const import API_VERSION_V1, PERSISTENT_VOLUME_CLAIM_KIND


class V1PersistentVolumeClaim(BaseModel):
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
    spec: V1PersistentVolumeClaimSpec

    openapi_types = {
        'api_version': 'str',
        'kind': 'str',
        'metadata': 'V1ObjectMeta',
        'spec': 'V1PersistentVolumeClaimSpec',
        # 'status': 'V1PersistentVolumeClaimStatus'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'kind': 'kind',
        'metadata': 'metadata',
        'spec': 'spec',
        # 'status': 'status'
    }

    @classmethod
    def default(cls, name: str, namespace: str, size: str, env: str, platform: str, sc: str):
        return cls.new(api_version=API_VERSION_V1, kind=PERSISTENT_VOLUME_CLAIM_KIND,
                       metadata=V1ObjectMeta.default(name=name, namespace=namespace, labels={"env": env,
                                                                                             "platform": platform}),
                       spec=V1PersistentVolumeClaimSpec.default(size=size, sc=sc))

    @staticmethod
    def new(api_version: str, kind: str, metadata: V1ObjectMeta, spec: V1PersistentVolumeClaimSpec):
        return V1PersistentVolumeClaim(api_version=api_version, kind=kind, metadata=metadata, spec=spec)
