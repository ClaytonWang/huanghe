# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Dict, Optional
from  basic.common.validator_name import  BaseModel_ValidatorName

class Namespace(BaseModel_ValidatorName):

    labels: Optional[Dict] = {"istio-injection": "enabled"}