from typing import Optional
from pydantic import BaseModel
from sqlalchemy import false

class TaskBody(BaseModel):

    # title:str
    # description: str
    # is_completed: bool = false
   

    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskResponseSchema(BaseModel):
    title:str
    is_completed: bool
    id:int