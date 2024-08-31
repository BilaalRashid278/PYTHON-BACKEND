from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlmodel import Session,select
from fastapi import Depends
from db.db import get_session
from models.model import User
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta

SECRET_KEY = "7832KJKLSDJFL23842937498237DNSDFKJSKF=SDFKJHSDFHS"
ALGORITHM = "HS256"
EXPIRY_TIME = 30

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes="bcrypt")

def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password,hash_password):
    return pwd_context.verify(password,hash_password)

def get_user_from_db(session : Annotated[Session,Depends(get_session)],username : str,email: str | None):
   user = session.exec(select(User).where(User.username == username)).first()
   if not user:
       user = session.exec(select(User).where(User.email == email)).first()
       if user:
           return user
   return user



async def authenticate_user(username,password,session : Annotated[Session,Depends(get_session)]):
    db_user = get_user_from_db(session,username=username,email='')
    if not db_user:
        return False
    if not verify_password(password=password,hash_password=db_user.password):
        return False
    return db_user
    

def create_access_token(data : dict,expiry_time : timedelta | None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(data_to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
