from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlmodel import Session,select
from fastapi import Depends
from db.db import get_session
from models.model import Todo,User


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes="bcrypt")

def hash_password(password):
    return pwd_context.hash(password)


def get_user_from_db(session : Annotated[Session,Depends(get_session)],username : str,email: str):
   user = session.exec(select(User).where(User.username == username)).first()
   if not user:
       user = session.exec(select(User).where(User.email == email)).first()
       if user:
           return user
   return user