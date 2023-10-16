from fastapi import FastAPI, Header, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select

import os
from controleur import Contoleur,Question,User

app = FastAPI()

controle = Contoleur()
    

@app.post("/questions/", name = "Creation du utilis")
def create_question(Authorization:Header(),question: Question):
    return 

@app.post("/users/",name="Creation d'un utilisateur")
def create_question(Authorization:Header(),user: User):       
        return 