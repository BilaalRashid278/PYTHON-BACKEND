from fastapi import FastAPI,Depends
from fastapi.routing import APIRoute
from fastapi.requests import Request
from sqlalchemy import create_engine
from settings import DEBUG,DATABASE_URL
from models.model import Todo
from sqlmodel import SQLModel,Session
from typing import Annotated


# connect application with postgresql database
connection_string : str = str(DATABASE_URL)
engine = create_engine(connection_string,echo=True)

# Create All Table like model is a table 
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def home(request: Request):
    return "Welcome to Todo Application"

app = FastAPI(debug=DEBUG,routes=[
    APIRoute('/',home)
])


@app.post('/todo/new',response_model=Todo)
async def Work(todo: Todo,session : Annotated[Session,Depends(get_session)]):
    try:
        session.add(todo)
        session.commit()
        session.refresh(todo)  
        return todo
    except :
        return {'message' : 'Todo not Added'}
    

@app.get('/todos')
async def get_todos():
    pass
@app.get('/todo/{id}')
async def get_todos():
    pass



