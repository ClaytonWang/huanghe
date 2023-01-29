import requests


class PrometheusQuery:
    def __init__(self, address: str):
        self.address = address

    def query(self, sql: str):
        return requests.get(f"{self.address}?query={sql}")





pq = PrometheusQuery("https://prometheus.digitalbrain.cn:32443/api/v1/query")
res = pq.query("kube_configmap_info")
print(res.json())