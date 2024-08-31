from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from settings import DEBUG
from models.model import Todo,Token,TokenData,User, TodoSub
from sqlmodel import Session,select
from db.db import get_session,create_tables
from typing import Annotated
from router.user import user_router
import uvicorn
from auth.auth import authenticate_user,create_access_token,EXPIRY_TIME,oauth_scheme,SECRET_KEY,ALGORITHM,get_user_from_db
from datetime import timedelta
from jose import jwt,JWTError


app = FastAPI(debug=DEBUG,title='Todo Application')

app.include_router(router=user_router)

create_tables()

def currentUser(token : Annotated[str,Depends(oauth_scheme)],session : Annotated[Session,Depends(get_session)]):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token",headers={'www-Authenticate' : 'Bearer'})
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username : str | None = payload.get('sub')
        if username is None:
            return credential_exception
        token_data = TokenData(username=username)
    except:
        raise JWTError
    user = get_user_from_db(session, token_data.username, None)
    if not user:
        raise credential_exception
    return user


@app.post('/token',response_model=Token)
async def login(login_data : Annotated[OAuth2PasswordRequestForm,Depends()],session : Annotated[Session,Depends(get_session)]):
    user = await authenticate_user(login_data.username, login_data.password, session)
    if not user:
        raise HTTPException(status_code=404,detail="Invalid username or password")
    expiry_time = timedelta(minutes=EXPIRY_TIME)
    access_token = create_access_token({"sub" : login_data.username},expiry_time)
    return Token(access_token=access_token,token_type="bearer")


@app.post('/todo/new',response_model=Todo)
async def Work(currentUser : Annotated[User,Depends(currentUser)],todo: TodoSub,session : Annotated[Session,Depends(get_session)]):
    try:
        newTodo = Todo(content=todo.content, is_complete=todo.is_complete, user_id=currentUser.id)
        session.add(newTodo)
        session.commit()
        session.refresh(newTodo)
        return newTodo
    except :
        return {'message' : 'Todo not Added'}
    

@app.get('/todos',response_model=list[Todo])
async def get_todos(session : Annotated[Session,Depends(get_session)],currentUser : Annotated[User,Depends(currentUser)]):
    todos = session.exec(select(Todo).where(Todo.user_id == currentUser.user_id)).all()
    return todos


@app.get('/todo/{id}',response_model=Todo)
async def get_todos(id : int,session : Annotated[Session,Depends(get_session)]):
    todos = session.exec(select(Todo).where(Todo.id == id)).first()
    if todos :
        return todos
    else:
        raise HTTPException(status_code=404,detail='Task Not Found')


@app.put('/todo/update',response_model=Todo)
async def update_todo(todo : Todo,session : Annotated[Session,Depends(get_session)]):
    existing_todo = session.exec(select(Todo).where(Todo.id == todo.id)).first()
    if existing_todo:
        existing_todo.content = todo.content
        existing_todo.is_complete = todo.is_complete
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else :
      raise HTTPException(status_code=404,detail='Task Not Found')
    
@app.delete('/todo/delete/{id}',response_model=dict)
async def deleteTodo(id : int,session : Annotated[Session,Depends(get_session)]):
    deleteTodo = session.exec(select(Todo).where(Todo.id == id))
    if deleteTodo:
        session.delete(deleteTodo.one())
        session.commit()
        return {'message' : 'Task Sussessfully Deleted'}
    else:
        raise HTTPException(status_code=404,detail='Task Not Found')


if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=4400, reload=True, workers=1)


