from pydantic import BaseModel, validator
import re


class Cluster(BaseModel):
    cluster: str = "zk"

class BaseModelValidatorName(Cluster):
    name: str

    @validator('name')
    def name_must_contain_space(cls, v):
        if not v[0].isalpha():
            raise ValueError('名称请由字母开头')
        return v

    @validator('name')
    def name_include(cls, v):
        if not re.match('^[0-9a-zA-Z-]+$', v):
            raise ValueError('名称请由字母、数字、中划线组成')
        return v

