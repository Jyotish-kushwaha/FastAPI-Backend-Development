from argon2 import hash_password
from h11 import Request
from passlib import exc
from psycopg2 import Timestamp

from src.user.dtos import LoginSchema, UserSchema
from fastapi import APIRouter , Depends, HTTPException , status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.model import UserTable
from pwdlib import PasswordHash
from src.utils.settings import settings
import jwt
from jwt import InvalidTokenError
from datetime import datetime,timedelta

# these are the authentication methods 


password_hash = PasswordHash.recommended()
TIME_EXP=60


def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def regiser(body:UserSchema,db:Session=Depends(get_db)):
    is_user=db.query(UserTable).filter(UserTable.username==body.username).first()
    if is_user:
        raise HTTPException(400,detail="Username already exist!")
    
    is_user=db.query(UserTable).filter(UserTable.email==body.email).first()
    if is_user:
        raise HTTPException(400,detail="Email Address already exists!")
    
    hash_password=get_password_hash(body.password)
    new_user=UserTable(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user






def login(body: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(UserTable).filter(UserTable.username == body.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="username not found!")
    
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=400, detail="password is incorrect!")
    
    exp_time = datetime.now() + timedelta(seconds=TIME_EXP)
    print(exp_time)

    token = jwt.encode(
        {
            "_id": user.id,
            "exp": exp_time.timestamp()
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return {"token": token}




def is_authenticated(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        token = token.split(" ")[-1]
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = data.get("_id")    
        user = db.query(UserTable).filter(UserTable.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are unauthorized")

        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are unauthorized")
