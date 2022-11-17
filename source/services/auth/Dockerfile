# syntax=docker/dockerfile:1.4

FROM ubuntu:20.04

# 定义时区
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai \
    LANG=C.UTF-8 \
    PYTHONPATH=/auth \
    PIP_CACHE_DIR=/.cache


ARG PROJECT_DIR=/auth

RUN mkdir $PROJECT_DIR

WORKDIR $PROJECT_DIR

# unbuntu dependence
RUN set -eux \
 && apt-get update \
 && apt-get install --no-install-recommends --no-install-suggests -y \
    build-essential postgresql-client python3.8 python3-pip python3.8-dev \
    uwsgi git libxml2-dev libxslt-dev zlib1g-dev


# python dependence
COPY requirements.txt $PROJECT_DIR
#RUN pip install --upgrade pip &&
RUN pip install -r $PROJECT_DIR/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . $PROJECT_DIR

EXPOSE 8000

ENTRYPOINT python main.py
#CMD ["/usr/local/bin/uwsgi", "--ini", "/opt/orange-backend/uwsgi.ini"]

