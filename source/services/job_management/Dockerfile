#python3.11
ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-job:2023-02-24.6
FROM $BASE_IMG

COPY services/job_management .
COPY basic /source/basic/

ENTRYPOINT python3 main.py