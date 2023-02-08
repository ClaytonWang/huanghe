# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/31 20:24
@Auth ： Z01
@File ：node_mixin.py
@Motto：You are the best!
"""
from k8s.api.core import Core
from k8s.api.core_v1_api import CoreV1Api
from k8s.model.v1_status import V1Status
class NodeMixin(CoreV1Api):
    def __init__(self, c: Core):
        super(NodeMixin, self).__init__(c=c)
    def list_node(self,):
        nodes = []
        response = self.core_v1_api.list_node_with_http_info()
        print()
        return self.core_v1_api.list_node_with_http_info()

# if __name__ == '__main__':
#     n=NodeMixin()