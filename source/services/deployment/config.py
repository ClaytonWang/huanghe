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


APP_NAME = Path(__file__).parent.name
BASIC_PATH = Path.joinpath(Path(__file__).parent.parent.parent, 'basic')
SOURCE_PATH = Path.joinpath(Path(BASIC_PATH).parent)
sys.path.insert(0, SOURCE_PATH.__str__())
K8S_YAML_CONFIG_PATH = '/etc/juece/config.yaml'
# 要在base.config目录下添加app文件
COMMON_CONFIG_PATH = 'basic.common.base_config'


try:
    common_module = importlib.import_module(COMMON_CONFIG_PATH)
    for key in common_module.__dict__:
        if key.startswith('__'):
            continue
        val = getattr(common_module, key)
        locals().__setitem__(key, val)
except ModuleNotFoundError:
    pass


DEBUG = True
SERVICE_PORT = 8000
DO_NOT_AUTH_URI = ['/auth/login', '/docs', '/openapi', '/openapi.json']
# NO_AUTH_WORDS = ['events', "status_update", "project_backend", "by_server"]


if os.path.exists(K8S_YAML_CONFIG_PATH):
    try:
        with open(K8S_YAML_CONFIG_PATH) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            locals().update(**data)
    except Exception as e:
        print(f'Loading k8s config error. {e}')
