# coding: utf-8
import datetime
import ujson as json

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkaom.v2.region.aom_region import AomRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkaom.v2 import *


class Chart:
    def __init__(self, name, time_data, value_data, unit):
        self.name = name
        self.time_data = time_data
        self.value_data = value_data
        self.unit = unit

    def __str__(self):
        return f"Chart(name='{self.name}', time_data={self.time_data}, value_data={self.value_data},unit='{self.unit}')"


def unix_to_datetime(unix_time):
    return (datetime.datetime.utcfromtimestamp(unix_time / 1000) + datetime.timedelta(hours=8)).strftime(
        '%Y-%m-%d %H:%M:%S')


def datetime_to_unix(datetime_str):
    dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return int(dt.timestamp() * 1000)

# print(datetime('2023-03-27 14:23:47'))
def minutes_between(start_time, end_time):
    start_dt = datetime.datetime.fromtimestamp(start_time / 1000)
    end_dt = datetime.datetime.fromtimestamp(end_time / 1000)
    diff = end_dt - start_dt
    minutes = diff.total_seconds() / 60
    return int(minutes)


def get_chart_hw(start_time, end_time):
    credentials = BasicCredentials("MKYKEUHIABSSLIULE9JR", "q5Coe7UrQPJbaa2nc1FbpQf3yRthQSD57ufwRJXx") \

    client = AomClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(AomRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = ListSampleRequest()
        request.fill_value = "0"
        listStatisticsbody = [
            "average"
        ]
        listDimensionsSamples = [
            DimensionSeries(
                name="appName",
                value="cci-deployment-202332101"
            )
        ]
        listSamplesbody = [
            QuerySample(
                namespace="PAAS.CONTAINER",
                dimensions=listDimensionsSamples,
                metric_name="cpuUage"
            ),
            QuerySample(
                namespace="PAAS.CONTAINER",
                dimensions=listDimensionsSamples,
                metric_name="memUsage"
            ),
            QuerySample(
                namespace="PAAS.CONTAINER",
                dimensions=listDimensionsSamples,
                metric_name="recvBytesRate"
            ),
            QuerySample(
                namespace="PAAS.CONTAINER",
                dimensions=listDimensionsSamples,
                metric_name="sendBytesRate"
            ),
            QuerySample(
                namespace="PAAS.CONTAINER",
                dimensions=listDimensionsSamples,
                metric_name="gpuUtil"
            )
        ]
        unix_start_time = datetime_to_unix(start_time)
        unix_end_time = datetime_to_unix(end_time)

        duration = minutes_between(unix_start_time, unix_end_time)
        period = 60 if duration <= 1200 else 300
        request.body = QuerySampleParam(
            time_range=str(unix_start_time) + '.' + str(unix_end_time) + '.' + str(duration),
            period=period if duration < 3600 else 900,
            # period=100,
            statistics=listStatisticsbody,
            samples=listSamplesbody
        )
        response = client.list_sample(request)
        chart_objects = []
        for sp in response.samples:
            chart_name = sp.sample.metric_name
            chart_unit = sp.data_points[0].unit
            chart_time = []
            chart_value = []
            for data in sp.data_points:
                if data.statistics[0].value != -1:
                    chart_time.append(unix_to_datetime(data.timestamp))
                    chart_value.append(data.statistics[0].value)
            chart_object = Chart(chart_name, chart_time, chart_value, chart_unit)
            response_chart = vars(chart_object)
            response_chart["data"] = [response_chart['time_data'], response_chart['value_data']]
            response_chart.pop("time_data")
            response_chart.pop("value_data")
            chart_objects.append(response_chart)
        chart_objects[0]["name"] = "CPU使用率"
        chart_objects[0]["unit"] = "Percent"
        chart_objects[1]["name"] = "Memory使用率"
        chart_objects[2]["name"] = "网络接收速率"
        chart_objects[3]["name"] = "网络发送速率"
        chart_objects[4]["name"] = "GPU使用率"
        # print(chart_objects)
        return chart_objects
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
get_chart_hw("2023-03-21 08:05:00", "2023-03-21 08:06:00")
def get_log_hw(index):
    ak = "MKYKEUHIABSSLIULE9JR"
    sk = "q5Coe7UrQPJbaa2nc1FbpQf3yRthQSD57ufwRJXx"

    credentials = BasicCredentials(ak, sk) \

    client = AomClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(AomRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = ListLogItemsRequest()
        request.type = "querylogs"
        searchKeybody = SearchKey(
            app_name="coredns",
            cluster_id="CCI-ClusterID",
            name_space="changjiang-notebook"
        )
        request.body = QueryBodyParam(
            start_time=1679881900846,
            search_key=searchKeybody,
            end_time=1680121900846,
            category="app_log",
        )
        response = client.list_log_items(request)
        print(response.result)
        data = json.loads(response.result)
        log_list = [info['logContent'] for info in data['data']]
        if index == 1:
            data = log_list[:50]
        else:
            start = (index - 1) * 50
            end = index * 50
            data = log_list[start:end]
        return data
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

# get_log_hw(2)


