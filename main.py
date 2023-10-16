from typing import Optional, List

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question : str
    subject : str
    use : str
    correct : List[str]
    responseA : str
    responseB : str
    responseC : str
    responseD : Optional[str] = Field(default=None, index=True)
    remark : Optional[str] = Field(default=None, index=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str 
    user_password: str
    admin: bool

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/questions/")
def create_question(question: Question):
    with Session(engine) as session:
        session.add(question)
        session.commit()
        session.refresh(question)
        return question

@app.post("/users/")
def create_question(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return 