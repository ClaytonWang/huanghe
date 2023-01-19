#python3.8
#ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-cluster:2023-01-04.3
#python3.11
ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-cluster:2023-01-11.9
FROM $BASE_IMG

COPY services/cluster .
COPY basic /source/basic/

ENTRYPOINT python3 main.py
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]

