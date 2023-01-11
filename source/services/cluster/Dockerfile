#ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-cluster:2023-01-04.3
#FROM $BASE_IMG
#
#COPY services/cluster .
#COPY basic /source/basic/
#
#ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]


FROM mirekphd/python3.11-ubuntu22.04

ARG APP_PATH=services/cluster
WORKDIR /source/services/cluster

RUN sed -i s@/archive.ubuntu.com//@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get clean

RUN set -eux \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
        build-essential postgresql-client gcc libpq-dev libxml2-dev libxslt-dev zlib1g-dev

# python dependence
COPY ${APP_PATH}/requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ${APP_PATH} .
COPY basic /source/basic/

ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]


