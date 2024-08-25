from fastapi import FastAPI,Depends,HTTPException
from settings import DEBUG
from models.model import Todo
from sqlmodel import Session,select
from db.db import get_session,create_tables
from typing import Annotated
from router.user import user_router
import uvicorn

app = FastAPI(debug=DEBUG,title='Todo Application')

app.include_router(router=user_router)

create_tables()

@app.post('/login')
async def login():
    ...


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


