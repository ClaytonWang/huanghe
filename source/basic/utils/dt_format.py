# -*- coding: utf-8 -*-
"""
    >File    : dt_format.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/27 15:53
"""

from typing import Optional
from datetime import datetime
DAY_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def dt_to_string(dt: Optional[datetime], ft: str = None):
    if isinstance(dt, datetime):
        return dt.strftime(ft if ft else DATETIME_FORMAT)
    return ''


def format_null_as_str(data):
    """
    去除所有数据null值
    :param data:
    :return:
    """
    if isinstance(data, str):
        if data is None:
            return ''
    if isinstance(data, list):
        tmp = list()
        for d in data:
            if isinstance(d, dict):
                res = format_dict_null(d)
                tmp.append(res)
            else:
                tmp.append(d)
        return tmp

    if isinstance(data, dict):
        data = format_dict_null(data)
        return data


def format_dict_null(data):
    assert isinstance(data, dict), 'not a dict'
    for (k, v) in data.items():
        if isinstance(v, dict):
            data[k] = format_dict_null(v)
        elif isinstance(v, list):
            data[k] = format_null_as_str(v)
        elif v is None:
            data[k] = ''
    return data


def format_str2date(s, unit='day'):
    """
    Args:
        s:  需要转换的字符串
        unit:
    Returns:

    """
    if not isinstance(s, str):
        return ''

    try:
        if unit == 'day':
            _str = DAY_FORMAT
            return datetime.strptime(s, _str).date()
        else:
            _str = DATETIME_FORMAT
        return datetime.strptime(s, _str)
    except ValueError:
        return ''
