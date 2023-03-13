
"""
    >File    : config.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/15 13:44
"""
import os
import sys
import yaml
import importlib
from pathlib import Path

DEBUG = True
SERVICE_PORT = 8000
DO_NOT_AUTH_URI = ['/auth/login', '/docs', '/openapi', '/openapi.json']
NO_AUTH_WORDS = ['events']

APP_NAME = Path(__file__).parent.name
BASIC_PATH = Path.joinpath(Path(__file__).parent.parent.parent, 'basic')
SOURCE_PATH = Path.joinpath(Path(BASIC_PATH).parent)
sys.path.insert(0, SOURCE_PATH.__str__())
K8S_YAML_CONFIG_PATH = '/etc/juece/config.yaml'
COMMON_CONFIG_PATH = f'basic.config.{APP_NAME}'
SERVICE_CONFIG_PATH = 'basic.config.service_requests'


try:
    common_module = importlib.import_module(COMMON_CONFIG_PATH)
    for key in common_module.__dict__:
        if key.startswith('__'):
            continue
        val = getattr(common_module, key)
        locals().__setitem__(key, val)
except ModuleNotFoundError:
    pass


# 从服务间请求加载
try:
    service_module = importlib.import_module(SERVICE_CONFIG_PATH)
    for key in service_module.__dict__:
        if key.startswith('__'):
            continue
        val = getattr(service_module, key)
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