from typing import Optional, List

from fastapi import FastAPI, Header, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
import os

class Question(SQLModel, table=True):
    """Modélisation d'un question disponible dans l'application"""
    id: Optional[int] = Field(default=None, primary_key=True)
    question : str
    use : str
    correct : List[str]
    responseA : str
    responseB : str
    responseC : str
    responseD : Optional[str] = Field(default=None, index=True)
    remark : Optional[str] = Field(default=None, index=True)

class User(SQLModel, table=True):
    """Modélisation d'un user disponible dans l'application"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    user_password: str
    admin: bool

sqlite_file_name = "questions_users.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def is_admin(usrpwd:str):
    pass

@app.post("/questions/", name = "Creation du utilis")
def create_question(usrpwd:Header(),question: Question):
    if not is_admin(usrpwd):
        raise HTTPException(status_code=404, detail=f"The id {userid} has not been find to delete")
    with Session(engine) as session:
        session.add(question)
        session.commit()
        session.refresh(question)
        return question

@app.post("/users/",name="Creation d'un utilisateur")
def create_question(usrpwd:Header()user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return 