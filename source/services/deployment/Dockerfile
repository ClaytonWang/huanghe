#python3.11
ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.deployment:2023-04-12.45
FROM $BASE_IMG

COPY services/deployment .
COPY basic /source/basic/
RUN pip install  huaweicloudsdkaom
ENTRYPOINT python3 main.py