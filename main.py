from fastapi import FastAPI,Depends,HTTPException
from fastapi.requests import Request
from sqlalchemy import create_engine
from settings import DEBUG,DATABASE_URL
from models.model import Todo
from sqlmodel import SQLModel,Session,select
from typing import Annotated
import uvicorn
from contextlib import asynccontextmanager


# connect application with postgresql database
connection_string : str = str(DATABASE_URL)
engine = create_engine(connection_string,echo=True)


# Create All Table like model is a table 
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(debug=DEBUG,title='Todo Application')


@app.post('/todo/new',response_model=Todo)
async def Work(todo: Todo,session : Annotated[Session,Depends(get_session)]):
    try:
        session.add(todo)
        session.commit()
        session.refresh(todo)  
        return todo
    except :
        return {'message' : 'Todo not Added'}
    

@app.get('/todos',response_model=list[Todo])
async def get_todos(session : Annotated[Session,Depends(get_session)]):
    todos = session.exec(select(Todo)).all()
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
        session.refresh()
        return existing_todo
    else :
      raise HTTPException(status_code=404,detail='Task Not Found')


if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=3000, reload=True, workers=1)


