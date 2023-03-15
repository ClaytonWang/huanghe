# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkaom.v2.region.aom_region import AomRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkaom.v2 import *

if __name__ == "__main__":
    ak = "MKYKEUHIABSSLIULE9JR"
    sk = "q5Coe7UrQPJbaa2nc1FbpQf3yRthQSD57ufwRJXx"

    credentials = BasicCredentials(ak, sk) \

    client = AomClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(AomRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = ListSampleRequest()
        listStatisticsbody = [
            "average"
        ]
        listDimensionsSamples = [
            DimensionSeries(
                name="appID",
                value="5947a400-4c87-4088-9e4d-077af73301e1"
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
                metric_name="recvPackRate"
            ),
            QuerySample(
                namespace="PAAS.CONTAINER",
                dimensions=listDimensionsSamples,
                metric_name="gpuUtil"
            )
        ]
        request.body = QuerySampleParam(
            time_range="-1.-1.60",
            period=300,
            statistics=listStatisticsbody,
            samples=listSamplesbody

        )
        response = client.list_sample(request)
        print(response)
        print("``````````````````")
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)