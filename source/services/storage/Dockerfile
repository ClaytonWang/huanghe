# syntax=docker/dockerfile:1.4

ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-storage:2023-01-04.2
FROM $BASE_IMG

COPY services/storage .
COPY basic /source/basic/

ENTRYPOINT python3 main.py