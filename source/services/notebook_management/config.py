# -*- coding: utf-8 -*-
"""
    >File   : config.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/14 18:47
"""
import os
import sys
import yaml
import importlib
from pathlib import Path


DEBUG = True
SERVICE_PORT = 8000
DO_NOT_AUTH_URI = ['/auth/login', '/docs', '/openapi', '/openapi.json']
NO_AUTH_WORDS = ['events', "project_backend", "by_server"]


APP_NAME = Path(__file__).parent.name
BASIC_PATH = Path.joinpath(Path(__file__).parent.parent.parent, 'basic')
SOURCE_PATH = Path.joinpath(Path(BASIC_PATH).parent)
sys.path.insert(0, SOURCE_PATH.__str__())
K8S_YAML_CONFIG_PATH = '/etc/juece/config.yaml'
# 要在base.config目录下添加app文件
COMMON_CONFIG_PATH = f'basic.config.{APP_NAME}'

# USER_SERVICE_PATH = 'http://localhost:8000'
# USER_SERVICE_PATH = 'http://121.36.41.231:32767/api/v1/user'
# STORAGE_SERVICE_PATH = 'http://121.36.41.231:32767/api/v1/storages'
# K8S_SERVICE_PATH = 'http://121.36.41.231:32767/api/v1/cluster'

try:
    common_module = importlib.import_module(COMMON_CONFIG_PATH)
    # print('>>>>>>.')
    # print(common_module.__dict__)
    for key in common_module.__dict__:
        if key.startswith('__'):
            continue
        val = getattr(common_module, key)
        locals().__setitem__(key, val)
except ModuleNotFoundError:
    pass

DB_USER = 'root'
DB_PASSWORD = 'linshimima2!'
DB_NAME = 'huanghe_dev'
DB_HOST = '123.60.43.172'
DB_PORT = '5432'


if os.path.exists(K8S_YAML_CONFIG_PATH):
    try:
        with open(K8S_YAML_CONFIG_PATH) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            locals().update(**data)
    except Exception as e:
        print(f'Loading k8s config error. {e}')
