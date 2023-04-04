# -*- coding: utf-8 -*-
"""
    >File   : serializers.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/14 15:49
"""
from services.cluster.namespace.serializers import Namespace
from services.cluster.network.serializers import Network


class PipelineDeleteReq():
    name: str
    namespace: str


class NamespacePipeline(Namespace, Network):

    def gen_namespace(self) -> Namespace:
        return Namespace.parse_obj(self)

    def gen_network(self) -> Network:
        return Network.parse_obj(self)


