from pydantic import BaseModel
from sqlalchemy import false
 
class UserSchema(BaseModel):
    name:str
    username:str
    password:str
    email:str

class UserResSchema(BaseModel):
    id : int    
    name:str
    username:str
    email:str

class LoginSchema(BaseModel):
    username:str
    password:str