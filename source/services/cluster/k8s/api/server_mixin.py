from services.cluster.k8s.api.core import K8sConfigFactory
from services.cluster.k8s.api.core_v1_api import CoreV1Api


def check_status(status_data):
    for condition in status_data:
        status = condition.type
        if "Pressure" in status:
            if condition.status == "True":
                return "False"
        if status == 'Ready':
            if condition.status == "True":
                return "Success"
            else:
                return "False"


def translate_memory(memory_data):
    return int(int(memory_data[:-2]) / (1024 * 1024))


class ServerMixin(CoreV1Api):
    def __init__(self, kcf: K8sConfigFactory):
        super(ServerMixin, self).__init__(kcf=kcf)

    def get_server_list(self):
        nodes = []
        response = self.core_v1_api().list_node_with_http_info()[0].items
        for node in response:
            server = node.metadata.name
            node_source_data = node.status.capacity
            server_ip = node.status.addresses[0].address
            cpu = node_source_data['cpu']
            memory = translate_memory(node_source_data['memory'])
            status = check_status(node.status.conditions)
            if not node_source_data.get("nvidia.com/gpu"):
                nodes.append({
                    'status': status,
                    'server_ip': server_ip,
                    'server_name': server,
                    'cpu': cpu,
                    'memory': memory,
                })
            else:
                gpu = node_source_data["nvidia.com/gpu"]
                type = node.metadata.labels["nvidia.com/gpu.product"].split("-")[1]
                nodes.append({
                    'status': status,
                    'server_ip': server_ip,
                    'server_name': server,
                    'cpu': cpu,
                    'gpu': gpu,
                    'memory': memory,
                    'type': type,
                })
        return nodes
