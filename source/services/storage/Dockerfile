#python3.8
#ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-storage:2023-01-04.2
#python3.11
ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-storage:2023-02-24.9
FROM $BASE_IMG

COPY services/storage .
COPY basic /source/basic/

ENTRYPOINT python3 main.py