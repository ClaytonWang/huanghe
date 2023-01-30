from pydantic import BaseModel, validator
import re

class BaseModel_ValidatorName(BaseModel):
 name: str

 @validator('name')
 def name_must_contain_space(cls, v):
  if not v[0].isalpha():
   raise ValueError('名称请由字母开头')
  return v.title()

 @validator('name')
 def name_len_not_more_than_20(cls, v):
  if len(v)>20 :
   raise ValueError('长度请不超过20位')
  return v.title()

 @validator('name')
 def name_include(cls, v):
  if not re.match('^[0-9a-zA-Z-]+$', v):
   raise ValueError('名称请由字母、数字、中划线组成')
  return v.title()