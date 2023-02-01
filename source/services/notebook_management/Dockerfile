# syntax=docker/dockerfile:1.4

ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-notebook:2023-02-01.7
#ARG APP_PATH=services/notebook_management
FROM $BASE_IMG

COPY services/notebook_management .
COPY basic /source/basic/

RUN chmod a+x start_service.sh

CMD ["./start_service.sh"]
