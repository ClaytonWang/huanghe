#python3.11
ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-job:2023-03-06.9
FROM $BASE_IMG

COPY services/deployment .
COPY basic /source/basic/

ENTRYPOINT python3 main.py