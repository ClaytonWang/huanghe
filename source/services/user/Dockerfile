# syntax=docker/dockerfile:1.4

ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-user:2023-04-12.9
#ARG APP_PATH=services/user
FROM $BASE_IMG

COPY services/user .
COPY basic /source/basic/

ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]