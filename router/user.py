from fastapi import APIRouter,Depends,HTTPException
from models.model import RegisterUser
from typing import Annotated
from auth.auth import get_user_from_db
from sqlmodel import Session
from db.db import get_session
from models.model import User
from auth.auth import hash_password,oauth_scheme



user_router = APIRouter(
    prefix="/user",
    tags=['user'],
    responses={
        404 : {
            'detail' : 'Not Found'
        }
    }
)

@user_router.post('/register')
async def register_user(new_user : Annotated[RegisterUser,Depends()],session : Annotated[Session,Depends(get_session)]):
   user = get_user_from_db(session,new_user.username,new_user.email)
   if user:
      raise HTTPException(status_code=409,detail="User already exsist")
   else:
      user = User(
         username=new_user.username,
         email=new_user.email,
         password=hash_password(new_user.password)
         )
      session.add(user)
      session.commit()
      session.refresh(user)
      return {'message' : f"User with {user.username} successfully registered...","success" : True}


# @user_router.get('/me')
# async def user_profile():
#    return 'Hello World'
      


