# -*- coding: utf-8 -*-

from pydantic import BaseModel, validator
from  basic.common.validator_name import  BaseModelValidatorName





class Pod(BaseModelValidatorName):
    namespace: str

