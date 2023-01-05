# syntax=docker/dockerfile:1.4

ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-user:2023-01-05.1
ARG APP_PATH=services/user
FROM $BASE_IMG

COPY ${APP_PATH} .
COPY basic /source/basic/

ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]