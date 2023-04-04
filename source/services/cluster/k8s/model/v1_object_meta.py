# coding: utf-8
from __future__ import annotations as anno
from services.cluster.k8s.model.generic_mixin import GenericMixin
from services.cluster.k8s.const.crd_kubeflow_const import ISTIO_DISABLE_INJECT_ANNOTATION, \
    HUAWEICLOUD_GPU_NAMESPACE_ANNOTATION, HUAWEICLOUD_CPU_NAMESPACE_ANNOTATION, HUAWEICLOUD_ENTERPRISE_PROJECT_LABEL,\
    HUAWEICLOUD_NETWORK_ANNOTATION, HUAWEICLOUD_INGRESS_ELB_PORT_ANNOTATION, HUAWEICLOUD_INGRESS_ANNOTATION
from typing import Optional, List, Dict
from datetime import datetime


class V1ObjectMeta(GenericMixin):
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
    name: str
    """
    Name must be unique within a namespace. Is required when creating resources, although some resources may allow a client to request the generation of an appropriate name automatically. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/identifiers#names  # noqa: E501
    """

    namespace: Optional[str]
    """
    Namespace defines the space within which each name must be unique. An empty namespace is equivalent to the \"default\" namespace, but \"default\" is the canonical representation. Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty.  Must be a DNS_LABEL. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/namespaces  # noqa: E501
    """

    annotations: Optional[Dict[str, str]]
    """
    Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. They are not queryable and should be preserved when modifying objects. More info: http://kubernetes.io/docs/user-guide/annotations  # noqa: E501
    """
    creation_timestamp: Optional[datetime]
    """
    CreationTimestamp is a timestamp representing the server time when this object was created. It is not guaranteed to be set in happens-before order across separate operations. Clients may not set this value. It is represented in RFC3339 form and is in UTC.  Populated by the system. Read-only. Null for lists. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa: E501
    """
    deletion_grace_period_seconds: Optional[int]
    """
    Number of seconds allowed for this object to gracefully terminate before it will be removed from the system. Only set when deletionTimestamp is also set. May only be shortened. Read-only.  # noqa: E501
    """
    deletion_timestamp: Optional[datetime]
    """
    DeletionTimestamp is RFC 3339 date and time at which this resource will be deleted. This field is set by the server when a graceful deletion is requested by the user, and is not directly settable by a client. The resource is expected to be deleted (no longer visible from resource lists, and not reachable by name) after the time in this field, once the finalizers list is empty. As long as the finalizers list contains items, deletion is blocked. Once the deletionTimestamp is set, this value may not be unset or be set further into the future, although it may be shortened or the resource may be deleted prior to this time. For example, a user may request that a pod is deleted in 30 seconds. The Kubelet will react by sending a graceful termination signal to the containers in the pod. After that 30 seconds, the Kubelet will send a hard termination signal (SIGKILL) to the container and after cleanup, remove the pod from the API. In the presence of network partitions, this object may still exist after this timestamp, until an administrator or automated process can determine the resource is fully terminated. If not set, graceful deletion of the object has not been requested.  Populated by the system when a graceful deletion is requested. Read-only. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa: E501

    """

    finalizers: Optional[List[str]]
    """
    Must be empty before the object is deleted from the registry. Each entry is an identifier for the responsible component that will remove the entry from the list. If the deletionTimestamp of the object is non-nil, entries in this list can only be removed. Finalizers may be processed and removed in any order.  Order is NOT enforced because it introduces significant risk of stuck finalizers. finalizers is a shared field, any actor with permission can reorder it. If the finalizer list is processed in order, then this can lead to a situation in which the component responsible for the first finalizer in the list is waiting for a signal (field value, external system, or other) produced by a component responsible for a finalizer later in the list, resulting in a deadlock. Without enforced ordering finalizers are free to order amongst themselves and are not vulnerable to ordering changes in the list.  # noqa: E501

    """
    generate_name: Optional[str]
    """
    GenerateName is an optional prefix, used by the server, to generate a unique name ONLY IF the Name field has not been provided. If this field is used, the name returned to the client will be different than the name passed. This value will also be combined with a unique suffix. The provided value has the same validation rules as the Name field, and may be truncated by the length of the suffix required to make the value unique on the server.  If this field is specified and the generated name exists, the server will return a 409.  Applied only if Name is not specified. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#idempotency  # noqa: E501

    """
    generation: Optional[int]
    """
    A sequence number representing a specific generation of the desired state. Populated by the system. Read-only.  # noqa: E501
    """
    labels: Optional[Dict[str, str]]
    """
    Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and services. More info: http://kubernetes.io/docs/user-guide/labels  # noqa: E501
    """

    managed_fields: Optional[List[str]]  # changed it
    """
    ManagedFields maps workflow-id and version to the set of fields that are managed by that workflow. This is mostly for internal housekeeping, and users typically shouldn't need to set or understand this field. A workflow can be the user's name, a controller's name, or the name of a specific apply path like \"ci-cd\". The set of fields is always in the version that the workflow used when modifying the object.  # noqa: E501
    """

    owner_references: Optional[str]  # changed it
    """
    list of objects depended by this object. If ALL objects in the list have been deleted, this object will be garbage collected. If this object is managed by a controller, then an entry in this list will point to this controller, with the controller field set to true. There cannot be more than one managing controller.  # noqa: E501
    """
    resource_version: Optional[str]
    """
    An opaque value that represents the internal version of this object that can be used by clients to determine when objects have changed. May be used for optimistic concurrency, change detection, and the watch operation on a resource or set of resources. Clients must treat these values as opaque and passed unmodified back to the server. They may only be valid for a particular resource or set of resources.  Populated by the system. Read-only. Value must be treated as opaque by clients and . More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency  # noqa: E501

    """
    self_link: Optional[str]
    """
    Deprecated: selfLink is a legacy read-only field that is no longer populated by the system.  # noqa: E501
    
    """
    uid: Optional[str]
    """
    UID is the unique in time and space value for this object. It is typically generated by the server on successful creation of a resource and is not allowed to change on PUT operations.  Populated by the system. Read-only. More info: http://kubernetes.io/docs/user-guide/identifiers#uids  # noqa: E501
    
    """

    openapi_types = {
        'annotations': 'dict(str, str)',
        'creation_timestamp': 'datetime',
        'deletion_grace_period_seconds': 'int',
        'deletion_timestamp': 'datetime',
        'finalizers': 'list[str]',
        'generate_name': 'str',
        'generation': 'int',
        'labels': 'dict(str, str)',
        'managed_fields': 'list[V1ManagedFieldsEntry]',
        'name': 'str',
        'namespace': 'str',
        'owner_references': 'list[V1OwnerReference]',
        'resource_version': 'str',
        'self_link': 'str',
        'uid': 'str'
    }

    attribute_map = {
        'annotations': 'annotations',
        'creation_timestamp': 'creationTimestamp',
        'deletion_grace_period_seconds': 'deletionGracePeriodSeconds',
        'deletion_timestamp': 'deletionTimestamp',
        'finalizers': 'finalizers',
        'generate_name': 'generateName',
        'generation': 'generation',
        'labels': 'labels',
        'managed_fields': 'managedFields',
        'name': 'name',
        'namespace': 'namespace',
        'owner_references': 'ownerReferences',
        'resource_version': 'resourceVersion',
        'self_link': 'selfLink',
        'uid': 'uid'
    }

    def set_annotations(self, annotations=None):
        if not annotations:
            annotations = []
        self.annotations = annotations
        return self

    def extend_annotations(self, annotations=None):
        if not self.annotations:
            self.annotations = {}
        if not annotations:
            annotations = {}
        self.annotations.update(annotations)
        return self

    def extend_labels(self, labels=None):
        if not self.labels:
            self.labels = {}
        if not labels:
            labels = {}
        self.labels.update(labels)
        return self

    @classmethod
    def default(cls, name, namespace=None, annotations=None, labels=None):
        return cls.new(name=name, namespace=namespace, annotations=annotations, labels=labels)

    @classmethod
    def without_istio_injection(cls, name, namespace=None, annotations=None, labels=None):
        meta = cls.new(name=name, namespace=namespace, annotations=annotations, labels=labels)
        meta.extend_annotations(ISTIO_DISABLE_INJECT_ANNOTATION)
        return meta

    @classmethod
    def huaweicloud_gpu_namespace(cls, name, namespace=None, annotations=None, labels=None):
        meta = cls.new(name=name, namespace=namespace, annotations=annotations, labels=labels)
        meta.extend_annotations(HUAWEICLOUD_GPU_NAMESPACE_ANNOTATION)
        meta.extend_labels(labels=HUAWEICLOUD_ENTERPRISE_PROJECT_LABEL)
        return meta

    @classmethod
    def huaweicloud_cpu_namespace(cls, name, namespace=None, annotations=None, labels=None):
        meta = cls.new(name=name, namespace=namespace, annotations=annotations, labels=labels)
        meta.extend_annotations(HUAWEICLOUD_CPU_NAMESPACE_ANNOTATION)
        meta.extend_labels(labels=HUAWEICLOUD_ENTERPRISE_PROJECT_LABEL)
        return meta

    @classmethod
    def huaweicloud_network(cls, name, namespace, annotations=None, labels=None):
        meta = cls.new(name=name, namespace=namespace, annotations=annotations, labels=labels)
        meta.extend_annotations(HUAWEICLOUD_NETWORK_ANNOTATION)
        return meta

    @classmethod
    def huaweicloud_ingress(cls, name, namespace, port, annotations=None, labels=None):
        meta = cls.new(name=name, namespace=namespace, annotations=annotations, labels=labels)
        meta.extend_annotations(HUAWEICLOUD_INGRESS_ANNOTATION)
        meta.extend_annotations({HUAWEICLOUD_INGRESS_ELB_PORT_ANNOTATION: port})
        return meta


    @staticmethod
    def new(name: str, namespace: str, annotations: Dict[str, str], labels: Dict[str, str]):
        return V1ObjectMeta(name=name, namespace=namespace, annotations=annotations, labels=labels)
