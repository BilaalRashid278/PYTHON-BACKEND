from sqlmodel import SQLModel,Field
from typing import Annotated

class Todo(SQLModel,table=True):
    __tablename__ = 'todo'
    id : int | None = Field(default=None,primary_key=True)
    content : str = Field(index=True,min_length=10,max_length=54)
    is_complete : bool = Field(default=False)