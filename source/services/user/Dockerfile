# syntax=docker/dockerfile:1.4

FROM ubuntu:20.04

ARG PROJECT_DIR=/source/services/auth
WORKDIR $PROJECT_DIR

RUN set -eux \
 && apt-get update \
 && apt-get install --no-install-recommends --no-install-suggests -y \
    build-essential postgresql-client gcc libpq-dev python3.8 python3-pip python3.8-dev \
    libxml2-dev libxslt-dev zlib1g-dev

# python dependence
COPY ./requirements.txt $PROJECT_DIR
RUN pip install -r $PROJECT_DIR/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . $PROJECT_DIR
COPY --from=source_basic . /source/basic/

EXPOSE 8000
ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]


