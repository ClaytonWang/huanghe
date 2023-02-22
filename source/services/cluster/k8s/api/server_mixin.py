from k8s.api.core import Core
from k8s.api.core_v1_api import CoreV1Api


def check_status(status_data):
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


def translate_memory(memory_data):
    return int(int(memory_data[:-2]) / (1024 * 1024))


class ServerMixin(CoreV1Api):
    def __init__(self, c: Core):
        super(ServerMixin, self).__init__(c=c)

    def get_server_list(self):
        nodes = []
        response = self.core_v1_api.list_node_with_http_info()[0].to_dict()
        for node in response['items']:
            server = node['metadata']['name']
            node_source_data = node['status']['capacity']
            cpu = node_source_data['cpu']
            memory = translate_memory(node_source_data['memory'])
            status = check_status(node['status']['conditions'])
            if node_source_data.get("nvidia.com/gpu") is None:
                nodes.append({
                    'status': status,
                    'serverIP': server,
                    'cpu': cpu,
                    'memory': memory,
                })
            else:
                gpu = node_source_data["nvidia.com/gpu"]
                type = node["metadata"]["labels"]["nvidia.com/gpu.product"].split("-")[1]
                nodes.append({
                    'status': status,
                    'serverIP': server,
                    'cpu': cpu,
                    'gpu': gpu,
                    'memory': memory,
                    'type': type,
                })
        return nodes
