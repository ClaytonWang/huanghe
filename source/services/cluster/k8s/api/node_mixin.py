from k8s.api.core import Core
from k8s.api.core_v1_api import CoreV1Api
from source.services.monitor.node.serializers import NodeCreate
from source.services.monitor.models.node import Node
from basic.middleware.rsp import success_common_response


class NodeMixin(CoreV1Api):
    def __init__(self, c: Core):
        super(NodeMixin, self).__init__(c=c)

    async def get_node_list(self, ncr: NodeCreate):
        nodes = []
        response = self.core_v1_api.list_node_with_http_info()[0].to_dict()
        for node in response['items']:
            ncr.server = node['metadata']['name']
            node_source_data = node['status']['capacity']
            ncr.cpu = node_source_data['cpu']
            ncr.memory = self.translate_memory(node_source_data['memory'])
            ncr.status = self.check_status(node['status']['conditions'])
            if node_source_data.get("nvidia.com/gpu") is None:
                nodes.append({
                    'status': ncr.status,
                    'server': ncr.server,
                    'source': f"CPU {ncr.cpu}C {ncr.memory}G"
                })
            else:
                ncr.gpu = node_source_data["nvidia.com/gpu"]
                ncr.type = node["metadata"]["labels"]["nvidia.com/gpu.product"].split("-")[1]
                nodes.append({
                    'status': ncr.status,
                    'server': ncr.server,
                    'source': f"GPU {ncr.gpu}*{ncr.type} {ncr.cpu}C {ncr.memory}G "
                })
            await self.create_node_database(ncr)
        return ncr

    async def create_node_database(self, ncr: NodeCreate):
        node = await Node.objects.get_or_none(server=ncr.server)
        if node is None:
            await Node.objects.create(**Node.gen_create_dict(ncr))
        else:
            await Node.objects.filter(server=ncr.server).update(status=ncr.status)
        return success_common_response()

    def translate_memory(self, memory_data):
        memory = (int)(memory_data[:-2])
        return (int)(memory / (1024 * 1024))

    def check_status(self, status_data):
        for condition in status_data:
            status = condition['type']
            if "Pressure" in status:
                if condition['status'] == "True":
                    return "False"
            if status == 'Ready':
                if condition['status'] == "True":
                    return "Success"
                else:
                    return "False"
