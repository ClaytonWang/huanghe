# -*- coding: utf-8 -*-

from basic.common.validator_name import BaseModelValidatorName


class PVCCreateReq(BaseModelValidatorName):
    namespace: str
    size: str
    # 对应环境
    env: str = "dev"
    platform: str = "mvp"


class PVCDeleteReq(BaseModelValidatorName):
    namespace: str
