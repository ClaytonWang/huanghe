# -*- coding: utf-8 -*-
"""
    >File   : service_mixin.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/9 20:27
"""
from __future__ import annotations

from typing import List

from services.cluster.k8s.api.core import Core
from services.cluster.k8s.model.v1_status import V1Status
from services.cluster.k8s.api.custom_object_api import CustomerObjectApi
from services.cluster.k8s.api.core_v1_api import CoreV1Api
from services.cluster.k8s.model.v1_service import V1Service
from typing import Dict
from services.cluster.service.serializers import ServiceDeleteReq, Service, ServiceQuery

import pprint


class ServiceMixin(CustomerObjectApi, CoreV1Api):
    def __init__(self, c: Core):
        super(ServiceMixin, self).__init__(c=c)

    def create_service(self, serv: Service) -> Dict:
        return self.core_v1_api.create_namespaced_service(namespace=serv.namespace,
                                                          body=V1Service.default(name=serv.name,
                                                                                 namespace=serv.namespace,
                                                                                 labels=serv.labels,
                                                                                 annotations=serv.annotations,
                                                                                 cluster_ip=serv.cluster_ip,
                                                                                 ports=serv.ports,
                                                                                 selector=serv.selector,
                                                                                 ),
                                                          )

    def delete_service(self, servdr: ServiceDeleteReq) -> V1Status:
        return self.core_v1_api.delete_namespaced_service(namespace=servdr.namespace,
                                                          name=servdr.name,)

    def list_service(self, servq: ServiceQuery):
        thread = self.core_v1_api.list_namespaced_service(namespace=servq.namespace)
        services = []
        for service in thread.items:
            metadata = service.metadata
            spec = service.spec
            _ports = spec.ports
            ports = []
            for port in spec.ports:
                ports.append({
                    "app_protocol": port.app_protocol,
                    "name": port.name,
                    "node_port": port.node_port,
                    "port": port.port,
                    "protocol": port.protocol,
                    "target_port": port.target_port,
                })
            services.append({
                "service_name": metadata.name,
                "namespace": metadata.namespace,
                "labels": metadata.labels,
                "self_link": metadata.self_link,
                "cluster_ip": spec.cluster_ip,
                "ports": ports,
                "selector": spec.selector,
                "type": spec.type,
            })
        # pprint.pprint(services)
        return services
