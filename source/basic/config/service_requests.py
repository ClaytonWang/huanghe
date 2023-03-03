# -*- coding: utf-8 -*-
"""
    >File   : service_requests.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/1 11:01
"""
import os
import sys
import yaml
import importlib
from pathlib import Path

# 用于集中服务间调用的URL配置

ENV_COMMON_NAMESPACE = "juece"
ENV_COMMON_AFTER = "svc.cluster.local"

DEBUG = True
SERVICE_PORT = 8000
DO_NOT_AUTH_URI = ['/auth/login', '/docs', '/openapi', '/openapi.json']

# MOCK
MOCK = os.getenv("MOCK_ACCOUNT_GETTER", False)
MOCK_USER_JSON = {"id": 60, 'username': "shouchen"}
MOCK_PROJECT_JSON = {"id": 1, "name": "决策平台"}
USER = "user"
ADMIN = "admin"
OWNER = "owner"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },

    "handlers": {
        "console": {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'verbose',
        }
    },
    "loggers": {
        'info': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'sqlalchemy.engine': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'databases': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
}

# user service
AUTH_PREFIX_URL = "/v1/auth/login"
USER_PREFIX_URL = "/user"
ACCOUNT_PREFIX_URL = "/user/account"
USER_ITEMS_URL = "/user/items"
PROJECT_PREFIX_URL = "/project"
PROJECT_ITEMS_URL = "/project/items"

CLUSTER_PVC_PREFIX_URL = "/pvc"
CLUSTER_NAMESPACE_PREFIX_URL = "/namespace"
CLUSTER_SECRET_PREFIX_URL = "/secret"
CLUSTER_VCJOB_PREFIX_URL = "/job"
CLUSTER_SERVER_PREFIX_URL = "/server"
CLUSTER_JOB_PREFIX_URL = "/job"

# storage
VOLUME_PREFIX_URL = "/volume"

# job
JOB_PREFIX_URL = "/jobs"
JOB_ITEMS_URL = "/jobs/items"

# notebooks
NOTEBOOK_PREFIX_URL = "/notebooks"
NOTEBOOK_ITEMS_URL = "/notebooks/items"
NOTEBOOK_VOLUME_PREFIX_URL = "/notebooks/volume"
NOTEBOOK_SOURCE_PREFIX_URL = "/source"
NOTEBOOK_IMAGE_PREFIX_URL = "/image"


USER_SERVICE_URL = f"user.{ENV_COMMON_NAMESPACE}.{ENV_COMMON_AFTER}"
CLUSTER_SERVICE_URL = f"cluster.{ENV_COMMON_NAMESPACE}.{ENV_COMMON_AFTER}"
STORAGE_SERVICE_URL = f"storage.{ENV_COMMON_NAMESPACE}.{ENV_COMMON_AFTER}"
NOTEBOOK_SERVICE_URL = f"notebook.{ENV_COMMON_NAMESPACE}.{ENV_COMMON_AFTER}"
JOB_SERVICE_URL = f"job.{ENV_COMMON_NAMESPACE}.{ENV_COMMON_AFTER}"
