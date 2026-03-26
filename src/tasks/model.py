from email.policy import default
from tokenize import String
from turtle import title

from fastapi.background import P
from sqlalchemy import  Column , Integer , String , Boolean
from src.utils.db import Base

class TaskModel(Base):
    __tablename__="user_task"
    id =Column(Integer, primary_key=True)
    title = Column(String) 
    description = Column(String)
    is_completed = Column(Boolean, default=False)

    