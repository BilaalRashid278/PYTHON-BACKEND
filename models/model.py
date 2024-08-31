from fastapi import Form
from sqlmodel import SQLModel,Field
from typing import Annotated
#from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

class Todo(SQLModel,table=True):
    __tablename__ = 'todo'
    id : int | None = Field(default=None,primary_key=True)
    content : str = Field(index=True,min_length=10,max_length=54)
    is_complete : bool = Field(default=False)
    user_id : int = Field(foreign_key="user.id")

class TodoSub(BaseModel):
    content: str = Field(index=True,min_length=10,max_length=54)
    is_complete: bool = Field(default=False)

class User(SQLModel,table=True):
    __tablename__ = 'user'
    id : int | None = Field(default=None,primary_key=True)
    username : str
    email : str
    password : str

class RegisterUser (BaseModel):
    username : Annotated[str,Form()]
    email : Annotated[str,Form()]
    password : Annotated[str,Form(min_length=8)]



class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
     username : str