from __future__ import annotations
from typing import List, Optional
from model.generic_mixin import GenericMixin
from model.v1_affinity import V1Affinity
from model.v1_container import V1Container
from model.v1_pod_dns_config import V1PodDNSConfig

class V1PodSpec(GenericMixin):
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
    active_deadline_seconds: Optional[int]
    affinity: Optional[V1Affinity]
    automount_service_account_token: Optional[bool]
    containers: List[V1Container]
    # dns_config: Optional[V1PodDNSConfig]
    # dns_policy: Optional[str]
    # enable_service_links: Optional[bool]
    # ephemeral_containers: Optional[L]
    openapi_types = {
        'active_deadline_seconds': 'int',
        'affinity': 'V1Affinity',
        'automount_service_account_token': 'bool',
        'containers': 'list[V1Container]',
        # 'dns_config': 'V1PodDNSConfig',
        # 'dns_policy': 'str',
        # 'enable_service_links': 'bool',
        # 'ephemeral_containers': 'list[V1EphemeralContainer]',
        # 'host_aliases': 'list[V1HostAlias]',
        # 'host_ipc': 'bool',
        # 'host_network': 'bool',
        # 'host_pid': 'bool',
        # 'host_users': 'bool',
        # 'hostname': 'str',
        # 'image_pull_secrets': 'list[V1LocalObjectReference]',
        # 'init_containers': 'list[V1Container]',
        # 'node_name': 'str',
        # 'node_selector': 'dict(str, str)',
        # 'os': 'V1PodOS',
        # 'overhead': 'dict(str, str)',
        # 'preemption_policy': 'str',
        # 'priority': 'int',
        # 'priority_class_name': 'str',
        # 'readiness_gates': 'list[V1PodReadinessGate]',
        # 'restart_policy': 'str',
        # 'runtime_class_name': 'str',
        # 'scheduler_name': 'str',
        # 'security_context': 'V1PodSecurityContext',
        # 'service_account': 'str',
        # 'service_account_name': 'str',
        # 'set_hostname_as_fqdn': 'bool',
        # 'share_process_namespace': 'bool',
        # 'subdomain': 'str',
        # 'termination_grace_period_seconds': 'int',
        # 'tolerations': 'list[V1Toleration]',
        # 'topology_spread_constraints': 'list[V1TopologySpreadConstraint]',
        # 'volumes': 'list[V1Volume]'
    }
    attribute_map = {
        'active_deadline_seconds': 'activeDeadlineSeconds',
        'affinity': 'affinity',
        'automount_service_account_token': 'automountServiceAccountToken',
        'containers': 'containers',
        'dns_config': 'dnsConfig',
        'dns_policy': 'dnsPolicy',
        'enable_service_links': 'enableServiceLinks',
        'ephemeral_containers': 'ephemeralContainers',
        'host_aliases': 'hostAliases',
        'host_ipc': 'hostIPC',
        'host_network': 'hostNetwork',
        'host_pid': 'hostPID',
        'host_users': 'hostUsers',
        'hostname': 'hostname',
        'image_pull_secrets': 'imagePullSecrets',
        'init_containers': 'initContainers',
        'node_name': 'nodeName',
        'node_selector': 'nodeSelector',
        'os': 'os',
        'overhead': 'overhead',
        'preemption_policy': 'preemptionPolicy',
        'priority': 'priority',
        'priority_class_name': 'priorityClassName',
        'readiness_gates': 'readinessGates',
        'restart_policy': 'restartPolicy',
        'runtime_class_name': 'runtimeClassName',
        'scheduler_name': 'schedulerName',
        'security_context': 'securityContext',
        'service_account': 'serviceAccount',
        'service_account_name': 'serviceAccountName',
        'set_hostname_as_fqdn': 'setHostnameAsFQDN',
        'share_process_namespace': 'shareProcessNamespace',
        'subdomain': 'subdomain',
        'termination_grace_period_seconds': 'terminationGracePeriodSeconds',
        'tolerations': 'tolerations',
        'topology_spread_constraints': 'topologySpreadConstraints',
        'volumes': 'volumes'
    }

    @classmethod
    def default(cls, name, image):
        return cls.new([V1Container.new(name=name, image=image)])


    @staticmethod
    def new(containers: List[V1Container]):
        return V1PodSpec(containers=containers)



if __name__ == '__main__':
    s = V1PodSpec()
    s.to_dict()