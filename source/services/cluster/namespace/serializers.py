# -*- coding: utf-8 -*-

from typing import Dict, Optional
from basic.common.validator_name import BaseModelValidatorName


class Namespace(BaseModelValidatorName):
    labels: Optional[Dict] = {"istio-injection": "enabled"}
