#python3.11
ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-deployment:2023-04-12.4
FROM $BASE_IMG

COPY services/deployment .
COPY basic /source/basic/

ENTRYPOINT python3 main.py
