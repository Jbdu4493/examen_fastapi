from fastapi import Body,FastAPI, HTTPException,Header
from pydantic import BaseModel
from typing import Optional, Annotated
import json
import pandas as pd 
import io
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
  "admin" : "4dm1N",
  "joe":"biz"
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
    
class Request_Subjects(BaseModel):
    subjects: list[str]
    nb_question: int

class Request_Use(BaseModel):
    use: str
    nb_question: int

api = FastAPI(title="My QCM",
    description="Examen FastAPI",
    version="1.0")

def check_usrpwd(user_name,user_password):
    password = users.get(user_name,None)
    return password == user_password

          
@api.get("/questions",name = "Retourn tout les questions disponible",
          responses ={200: {"description": "OK"},
                      401 : {"description":"User password incorrect"},
                      409: {"description": "No allow to add question"}})
def get_all(Authorization:str = Header()) -> list[Question]:
    """""Fonction permettant a un admin de voir toute les questions disponible """""
    user,password = Authorization.split(':')
    if user != "admin":
        raise  HTTPException(status_code=409,detail=f"The user '{user}' is not a admin user ")
    elif not check_usrpwd(user,password):
        raise  HTTPException(status_code=401,detail=f"User password incorrect")
    result = base_de_donnee.to_json(orient='records')
    return json.loads(result)


@api.post("/questions" ,
          name = "Creation d'un question",
          responses ={200: {"description": "OK"},
                      401 : {"description":"User password incorrect"},
                      409: {"description": "No allow to add question"}})
def create_question(question: Question,Authorization:str = Header()):
    global base_de_donnee
    """Fonction permettant a un admin de cree une question"""
    user,password = Authorization.split(':')
    if user != "admin":
        raise  HTTPException(status_code=409,detail=f"The user {user} is not admin ")
    elif not check_usrpwd(user,password):
        raise  HTTPException(status_code=401,detail=f"User password incorrect")
    data = json.dumps([question.__dict__])
    line_df = pd.read_json(io.StringIO(data))
    print(line_df)
    global base_de_donnee
    base_de_donnee =  pd.concat([base_de_donnee,line_df],axis=0)
    return {"detail":'OK'}


@api.get("/questions/use",name = "Retourn tout les questions disponible",
          responses ={200: {"description": "OK"},
                      401 : {"description":"User password incorrect"},
                      406: {"description": "Not enougth questions " }})
def get_qcm_by_use(request_use:Request_Use,Authorization:str = Header())-> list[Question]:
    user,password = Authorization.split(':')
    if not check_usrpwd(user,password):
        raise  HTTPException(status_code=401,detail=f"User password incorrect ")
    try:
        result = base_de_donnee[base_de_donnee.use == request_use.use ].sample(request_use.nb_question).to_json(orient='records')
    except ValueError:
        raise  HTTPException(status_code=406,detail=f"Request too restrictive to raise {request_use.nb_question} questions")
    return json.loads(result) 


@api.get("/questions/subjects",name = "Retourn tout les questions disponible",
          responses ={200: {"description": "OK"},
                      401 : {"description":"User password incorrect"},
                      406: {"description": "Not enougth questions " }})

def get_qcm_by_subjects(resquest_subjects: Request_Subjects ,Authorization:str = Header())-> list[Question]:
    user,password = Authorization.split(':')
    if not check_usrpwd(user,password):

        raise  HTTPException(status_code=401,detail=f"User password incorrect")
    try:
        result = base_de_donnee[base_de_donnee.subject.isin(resquest_subjects.subjects )].sample(resquest_subjects.nb_question).to_json(orient='records')
    except ValueError:
        raise  HTTPException(status_code=406,detail=f"Request too restrictive to raise {resquest_subjects.nb_question} questions")
    return json.loads(result) 
   
