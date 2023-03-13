# -*- coding: utf-8 -*-
"""
    >File   : config.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/7 20:29
"""

import os
import sys
import yaml
import importlib
from pathlib import Path
from basic.common.env_variable import get_string_variable


"""
项目基础信息配置
"""

APP_NAME = Path(__file__).parent.name
BASIC_PATH = Path.joinpath(Path(__file__).parent.parent.parent, 'basic')
SOURCE_PATH = Path.joinpath(Path(BASIC_PATH).parent)
sys.path.insert(0, SOURCE_PATH.__str__())
K8S_YAML_CONFIG_PATH = '/etc/juece/config.yaml'
COMMON_CONFIG_PATH = 'basic.common.base_config'

"""
加载公用配置 
"""
try:
    common_module = importlib.import_module(COMMON_CONFIG_PATH)
    for key in common_module.__dict__:
        if key.startswith('__'):
            continue
        val = getattr(common_module, key)
        locals().__setitem__(key, val)
    # print(locals())
except ModuleNotFoundError:
    pass


DO_NOT_AUTH_URI = ['/auth/login', '/docs', '/openapi', '/openapi.json']
NO_AUTH_WORDS = ['events', "status_update", "project_backend", "by_server"]


debug = False if 'PRODUCTION' == get_string_variable('ENV', 'DEV') else True

"""
加载服务器配置
"""
if os.path.exists(K8S_YAML_CONFIG_PATH):
    try:
        with open(K8S_YAML_CONFIG_PATH) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            locals().update(**data)
    except Exception as e:
        print(f'Loading k8s config error. {e}')
