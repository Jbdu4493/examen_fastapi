from fastapi import FastAPI, HTTPException,Header
from pydantic import BaseModel
from typing import Optional
import json
import pandas as pd 

def create_db():
    df =  pd.read_csv("https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv")
    df = df[~ df.correct.isna()]
    df.correct = df.correct.str.replace(',',' ')
    df.correct = df.correct.apply(lambda x: x.split(" "))
    return df

base_de_donnee = create_db()

users = { 
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine",
  "admin" : "4dm1N"
}
class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: list[str]
    responseA: str
    responseB: str
    responseC: Optional[str] = None
    responseD:Optional[str] = None
    remark: Optional[str] = None
    

api = FastAPI(title="My QCM",
    description="Examen FastAPI",
    version="1.0.1")
    

@api.post("/questions",
          name = "Creation d'un question",
          responses ={200: {"description": "OK"},
                     409: {"description": "No allow to add question"}})
def create_question(question: Question,Authorization:str = Header()):
    """Fonction permettant a un admin de cree une question"""
    return {"detail":'OK'}

@api.get("/questions",name = "Retourn tout les questions disponible",
          responses ={200: {"description": "OK"},
                     403: {"description": "No allow to get all questions"}})
def get_all(question: Question,Authorization:str = Header()):
    """""Fonction permettant a un admin de voir toute les questions disponible """""
    return {"detail":'OK'}


@api.get("/questions/use",name = "Retourn tout les questions disponible",
          responses ={200: {"description": "OK"},
                     403: {"description": "No allow to get question" },
                     406: {"description": "Not enougth questions" }})
def get_qcm_by_use(use: str, nb_question:int,Authorization:str = Header()):
    return {"detail":'OK'}


@api.get("/questions/subjects",name = "Retourn tout les questions disponible",
          responses ={200: {"description": "OK"},
                     403: {"description": "No allow to get question" },
                     406: {"description": "Not enougth questions" }})
def get_qcm_by_subjects(subjects: list[str], nb_question:int,Authorization:str = Header()):
    {"detail":'OK'}