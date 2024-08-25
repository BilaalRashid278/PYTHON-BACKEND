from sqlalchemy import create_engine
from sqlmodel import SQLModel,Session
from settings import DATABASE_URL

# connect application with postgresql database
connection_string : str = str(DATABASE_URL)
engine = create_engine(connection_string,echo=True)


def create_tables():
    # Create All Table like model is a table 
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
