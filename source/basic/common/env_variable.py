# -*- coding: utf-8 -*-
"""
    读取环境变量
    >File    : env_variable.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/27 10:39
"""
import os


def get_integer_variable(name: str, default: int = None) -> int:
    var = int(os.getenv(name.upper(), 0))
    return var if var else default


def get_string_variable(name: str, default: str = None) -> str:
    var = os.getenv(name.upper())
    return var if var else default

def get_lower_string_variable(name: str, default: str = None) -> str:
    return os.getenv(name, default).lower()