from k8s.model.generic_mixin import GenericMixin
from k8s.model.v1_object_meta import V1ObjectMeta
from typing import Optional

class BaseModel(GenericMixin):

    """
    Attributes:
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    api_version: str
    kind: str
    metadata: Optional[V1ObjectMeta]
    spec: object
    status: Optional[object]

    attribute_map = {
        'api_version': 'apiVersion',
        'kind': 'kind',
        'metadata': 'metadata',
        'spec': 'spec',
        'status': 'status'
    }





if __name__ == '__main__':
    b = BaseModel(api_version="ss", kind="sss")
    b.to_dict()