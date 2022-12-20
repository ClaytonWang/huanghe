# coding: utf-8
from __future__ import annotations
from k8s.model.base_model import BaseModel
from k8s.model.v1_notebook_spec import V1NotebookSpec
from k8s.model.v1_object_meta import V1ObjectMeta
from k8s.const.crd_kubeflow_const import KUBEFLOW_V1_API_VERSION, KUBEFLOW_NOTEBOOK_KIND

class V1Notebook(BaseModel):
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
    spec: V1NotebookSpec
    openapi_types = {
        'api_version': 'str',
        'kind': 'str',
        'metadata': 'V1ObjectMeta',
        'spec': 'V1NotebookSpec',
        # 'status': 'V1NotebookStatus'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'kind': 'kind',
        'metadata': 'metadata',
        'spec': 'spec',
        'status': 'status'
    }

    @classmethod
    def default(cls, name, namespace, image, env, platform):
        return cls.new(api_version=KUBEFLOW_V1_API_VERSION,
                       kind=KUBEFLOW_NOTEBOOK_KIND,
                       metadata=V1ObjectMeta.default(name=name, namespace=namespace, labels={
                           "env": env,
                           "platform": platform
                       }),
                       spec=V1NotebookSpec.default(name=name, image=image),
                       status=None)

    @staticmethod
    def new(api_version: str, kind: str, metadata: V1ObjectMeta, spec: V1NotebookSpec, status):
        return V1Notebook(api_version=api_version, kind=kind, metadata=metadata, spec=spec, status=status)