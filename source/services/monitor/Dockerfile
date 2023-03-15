#python3.11
ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.monitor:2023-03-15.194
FROM $BASE_IMG

COPY services/monitor .
COPY basic /source/basic/

RUN chmod a+x start_service.sh

CMD ["./start_service.sh"]