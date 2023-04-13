#python3.8
#ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-cluster:2023-01-04.3
#python3.11
ARG BASE_IMG=containers.git.digitalbrain.cn/engineering-group/huanghe.base-cluster:2023-04-13.24
FROM $BASE_IMG

COPY services/cluster .
COPY basic /source/basic/

# 华为云aksk
ARG AK=RABVMT0LW6WB2QSZNRVT
ARG SK=00SGlW1Y9970QGCI87eUgQO6SjBZfiNXKxWlbzP4
ENV AK=$AK
ENV SK=$SK


RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin

RUN chmod +x ./cci-iam-authenticator  \
    && mv ./cci-iam-authenticator /usr/local/bin  \
    && cci-iam-authenticator generate-kubeconfig --cci-endpoint=https://cci.cn-north-4.myhuaweicloud.com --ak=$AK --sk=$SK \
    && cp ~/.kube/config ./kubeconfig/hw

ENTRYPOINT python3 main.py
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]

