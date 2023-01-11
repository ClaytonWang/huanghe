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


# python dependence
COPY ${APP_PATH}/requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ${APP_PATH} .
COPY basic /source/basic/

ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]


