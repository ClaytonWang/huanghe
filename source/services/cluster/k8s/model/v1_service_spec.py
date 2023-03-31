# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Optional, List, Dict
from services.cluster.k8s.model.generic_mixin import GenericMixin
from services.cluster.k8s.model.v1_service_port import V1ServicePort


class V1ServiceSpec(GenericMixin):
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
    ports: List[V1ServicePort]
    cluster_ip: Optional[str]
    selector: Dict[str, str]

    openapi_types = {
        # 'allocate_load_balancer_node_ports': 'bool',
        'cluster_ip': 'str',
        # 'cluster_i_ps': 'list[str]',
        # 'external_i_ps': 'list[str]',
        # 'external_name': 'str',
        # 'external_traffic_policy': 'str',
        # 'health_check_node_port': 'int',
        # 'internal_traffic_policy': 'str',
        # 'ip_families': 'list[str]',
        # 'ip_family_policy': 'str',
        # 'load_balancer_class': 'str',
        # 'load_balancer_ip': 'str',
        # 'load_balancer_source_ranges': 'list[str]',
        'ports': 'list[V1ServicePort]',
        # 'publish_not_ready_addresses': 'bool',
        'selector': 'dict(str, str)',
        # 'session_affinity': 'str',
        # 'session_affinity_config': 'V1SessionAffinityConfig',
        # 'type': 'str'
    }

    attribute_map = {
        # 'allocate_load_balancer_node_ports': 'allocateLoadBalancerNodePorts',
        'cluster_ip': 'clusterIP',
        # 'cluster_i_ps': 'clusterIPs',
        # 'external_i_ps': 'externalIPs',
        # 'external_name': 'externalName',
        # 'external_traffic_policy': 'externalTrafficPolicy',
        # 'health_check_node_port': 'healthCheckNodePort',
        # 'internal_traffic_policy': 'internalTrafficPolicy',
        # 'ip_families': 'ipFamilies',
        # 'ip_family_policy': 'ipFamilyPolicy',
        # 'load_balancer_class': 'loadBalancerClass',
        # 'load_balancer_ip': 'loadBalancerIP',
        # 'load_balancer_source_ranges': 'loadBalancerSourceRanges',
        'ports': 'ports',
        # 'publish_not_ready_addresses': 'publishNotReadyAddresses',
        'selector': 'selector',
        'session_affinity': 'sessionAffinity',
        # 'session_affinity_config': 'sessionAffinityConfig',
        'type': 'type'
    }

    @classmethod
    def default(cls, selector):
        return cls.new(selector=selector, ports=[V1ServicePort.default()])

    @staticmethod
    def new(ports: List[V1ServicePort], selector: Dict[str, str]):
        return V1ServiceSpec(ports=ports, selector=selector)
