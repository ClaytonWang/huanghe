# syntax=docker/dockerfile:1.4

FROM digglerz/python3.8

ARG PROJECT_DIR=/source/services/cluster
WORKDIR $PROJECT_DIR



# python dependence
COPY ./requirements.txt $PROJECT_DIR
RUN pip install -r $PROJECT_DIR/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . $PROJECT_DIR

ENTRYPOINT python3 main.py
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]


