# -*- coding: utf-8 -*-
"""
    >File   : job_management.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/16 18:55
"""
import os
import sys
import yaml
import importlib
from pathlib import Path
SECRET_KEY = "dc393487a84ddf9da61fe0180ef295cf0642ecbc5d678a1589ef2e26b35fce9c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

ENV_COMMON_URL = "http://121.36.41.231:32767/api/v1"
# AUTH_PREFIX_URL = "/user/v1/auth/login"
# USER_PREFIX_URL = "/user/user"
# ACCOUNT_PREFIX_URL = "/user/user/account"
# PROJECT_PREFIX_URL = "/user/project"
# VOLUME_PREFIX_URL = "/storages/volume"
# CLUSTER_JOB_PREFIX_URL = "/cluster/job"
ENV_COMMON_NAMESPACE = "juece"
ENV_COMMON_AFTER = "svc.cluster.local"
AUTH_PREFIX_URL = "/v1/auth/login"
USER_PREFIX_URL = "/user"
ACCOUNT_PREFIX_URL = "/user/account"
PROJECT_PREFIX_URL = "/project"
VOLUME_PREFIX_URL = "/volume"
CLUSTER_PVC_PREFIX_URL = "/pvc"
CLUSTER_JOB_PREFIX_URL = "/notebook"
ENV = "uat"
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

DEBUG = True
SERVICE_PORT = 8000
DO_NOT_AUTH_URI = ['/auth/login', '/docs', '/openapi', '/openapi.json']

APP_NAME = Path(__file__).parent.name
BASIC_PATH = Path.joinpath(Path(__file__).parent.parent.parent, 'basic')
SOURCE_PATH = Path.joinpath(Path(BASIC_PATH).parent)
sys.path.insert(0, SOURCE_PATH.__str__())
K8S_YAML_CONFIG_PATH = '/etc/juece/config.yaml'
COMMON_CONFIG_PATH = f'basic.config.{APP_NAME}'

try:
    common_module = importlib.import_module(COMMON_CONFIG_PATH)
    for key in common_module.__dict__:
        if key.startswith('__'):
            continue
        val = getattr(common_module, key)
        locals().__setitem__(key, val)
except ModuleNotFoundError:
    pass


if os.path.exists(K8S_YAML_CONFIG_PATH):
    try:
        with open(K8S_YAML_CONFIG_PATH) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            locals().update(**data)
    except Exception as e:
        print(f'Loading k8s config error. {e}')

USER_SERVICE_URL = f"user.{ENV_COMMON_NAMESPACE}.{ENV_COMMON_AFTER}"
CLUSTER_SERVICE_URL = f"cluster.{ENV_COMMON_NAMESPACE}.{ENV_COMMON_AFTER}"
STORAGE_SERVICE_URL = f"storage.{ENV_COMMON_NAMESPACE}.{ENV_COMMON_AFTER}"

