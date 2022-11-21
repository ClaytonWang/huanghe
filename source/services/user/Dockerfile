# syntax=docker/dockerfile:1.4

FROM ubuntu:20.04

ENV TZ=Asia/Shanghai
ARG APP_PATH=services/user
WORKDIR /source/services/user

RUN sed -i s@/ports.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get clean
RUN set -eux \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
        build-essential postgresql-client gcc libpq-dev python3.8 python3-pip python3.8-dev \
        libxml2-dev libxslt-dev zlib1g-dev

# python dependence
COPY ${APP_PATH}/requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ${APP_PATH} .
COPY basic /source/basic/

EXPOSE 8000
ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]