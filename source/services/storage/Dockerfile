# syntax=docker/dockerfile:1.4

FROM digglerz/python3.8
ARG APP_PATH=services/storage
WORKDIR /source/services/storage


# python dependence
COPY ${APP_PATH}/requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ${APP_PATH} .
COPY basic /source/basic/

ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]