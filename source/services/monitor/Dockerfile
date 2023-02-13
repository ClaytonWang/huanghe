#python3.11
ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-monitor:2023-01-29.3
FROM $BASE_IMG

COPY services/monitor .
COPY basic /source/basic/

RUN chmod a+x start_service.sh

CMD ["./start_service.sh"]