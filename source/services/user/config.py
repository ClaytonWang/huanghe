# -*- coding: utf-8 -*-
"""
    >File    : config.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/15 13:44
"""
import os
import sys
import logging
from pathlib import Path
APP_NAME = 'user'
BASIC_PATH = Path.joinpath(Path(__file__).parent.parent.parent, 'basic')
SOURCE_PATH = Path.joinpath(Path(BASIC_PATH).parent)
sys.path.insert(0, SOURCE_PATH.__str__())

from basic.config.user import *
DO_NOT_AUTH_URI = ['/auth/login', '/docs', '/openapi']
SERVICE_PORT = 8000
DEBUG = True

DATABASES = {
    'USER': 'root',
    'PASSWORD': 'linshimima2!',
    'NAME': 'huanghe_dev',
    'HOST': '123.60.43.172',
    'PORT': '5432',
}


