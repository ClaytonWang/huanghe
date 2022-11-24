FROM digglerz/python3.8

ARG APP_PATH=services/cluster
WORKDIR /source/services/cluster


# python dependence
COPY ${APP_PATH}/requirements.txt .
RUN pip install -r $PROJECT_DIR/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ${APP_PATH} .

ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]


