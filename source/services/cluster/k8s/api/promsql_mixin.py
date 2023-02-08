# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/30 15:43
@Auth ： Z01
@File ：promsql_mixin.py
@Motto：You are the best!
"""
from utils.prometheus import pq



class PromSqlMixin():

    def list_node(self):
        ip_list = []
        sql="group by(internal_ip) (kube_node_info)"
        res = pq.query(sql)
        response = res.json()
        for ip in response["data"]["result"]:
            ip_list.append(ip["metric"]["internal_ip"])
        return ip_list



    def cpu_source_format(self, ip):
        sql = "instance:node_num_cpu:sum{instance='" + ip + ":9100'}"
        res = pq.query(sql)
        response = res.json()
        return response["data"]["result"][0]["value"][1]
        # return response
    def memory_source_format(self, ip):
        sql = "node_memory_MemTotal_bytes{instance='" + ip + ":9100'}/(1024*1024*1024)"
        res = pq.query(sql)
        response = res.json()
        return response["data"]["result"][0]["value"][1]

    def gpu_model_name(self,ip):
        sql="DCGM_FI_PROF_GR_ENGINE_ACTIVE"
        res = pq.query(sql)
        response = res.json()
        return response["data"]["result"][0]["metric"]["modelName"]

if __name__ == '__main__':
    p = PromSqlMixin()
    print(p.list_node())
    ip_list = p.list_node()
    # print(p.source_format("192.168.1.158"))
    for ip in ip_list:
        print(p.memory_source_format(ip))

