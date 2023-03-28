# -*- coding: utf-8 -*-

from basic.common.validator_name import BaseModelValidatorName, Cluster


class SecretCommon(BaseModelValidatorName):
    namespace: str


class SecretNamespace(Cluster):
    namespace: str
