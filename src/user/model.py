from pydantic import EmailStr
from sqlalchemy import Column,Integer,String,Boolean,DateTime, null
from src.utils.db import Base

class UserTable(Base):
    __tablename__="User_Table"
    id=Column(Integer,primary_key=True)
    name = Column(String)
    username = Column(String,nullable=False)
    email = Column(String)
    hash_password = Column(String , nullable=False)