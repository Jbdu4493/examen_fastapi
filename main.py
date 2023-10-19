from fastapi import Body,FastAPI, HTTPException,Header
from pydantic import BaseModel,constr, Field
from typing import Optional, Annotated,List
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
  "admin" : "4dm1N",
  "joe":"biz"
}
class Question(BaseModel):
    question: str =Field( description="Libelle de la question")
    subject: str =Field( description="Thème de la question")
    use: str 
    correct: list[str] = Field( description="Liste des bonne reponse ex. : 'A', 'B', 'C'  ou 'D' ")
    responseA: str = Field( description="La proposition A")
    responseB: str = Field( description="La proposition B ")
    responseC: Optional[str] = Field( default=None, description="La proposition C")
    responseD: Optional[str] = Field( default=None, description="La proposition D")
    remark: Optional[str] = Field( default=None, description="Remarque")
    
class Request_Subjects(BaseModel):
    subjects: list[str] = Field( description="Liste des sujets souhaités")
    nb_question: int = Field(gt=0, description="Nombre de question souhaité")

class Request_Use(BaseModel):
    use: str = Field( description="Use")
    nb_question: int = Field(gt=0, description="Nombre de question souhaité")

class Utilisateur(BaseModel):
    user_name: str = Field( description="Identifant de l'utilisateur")
    password: str  = Field( description="Mot de passe")


api = FastAPI(title="My QCM",
    description="Examen FastAPI",
    version="1.0",
    openapi_tags=[
    {
        'name': 'utilisateur',
        'description': 'Fonctionnalité dediée à la gestion utilisateur'
    },
    {
        'name': 'question',
        'description': 'Fonctionnalité dediée à la gestion des question'
    },
    
    {
        'name': 'admin',
        'description': "Fonctionnalité dediée à l'admin"
    }
])
    



def check_usrpwd(user_name,user_password):
    password = users.get(user_name,None)
    return password == user_password


@api.post("/users" ,
          name = "Creation d'un utilisateur",
          responses ={200: {"description": "OK"},
                      401 : {"description":"User password incorrect"},
                      409: {"description": "No allow to add question"}},
          tags=['utilisateur','admin']  )
async def create_user(utilisateur: Utilisateur,Authorization:str = Header()):
    """Fonction permettant a un admin de cree une utilisateur"""
    user,password = Authorization.split(':')
    if user != "admin":
        raise  HTTPException(status_code=409,detail=f"The user {user} is not admin ")
    elif not check_usrpwd(user,password):
        raise  HTTPException(status_code=401,detail=f"User password incorrect")
    global users
    users[utilisateur.user_name] = utilisateur.password
    return {"detail":'OK'}

@api.get("/users",name = "Retourne tout les utilisateur disponible",
          responses ={200: {"description": "OK"},
                      401 : {"description":"User password incorrect"},
                      409: {"description": "No allow to add question"}},
          tags=['utilisateur','admin'] )
async def get_all_user(Authorization:str = Header()) -> list[Utilisateur]:
    """""Fonction permettant a un admin de voir toute les utilisateur """""
    user,password = Authorization.split(':')
    if user != "admin":
        raise  HTTPException(status_code=409,detail=f"The user '{user}' is not a admin user ")
    elif not check_usrpwd(user,password):
        raise  HTTPException(status_code=401,detail=f"User password incorrect")
    
    return users

          
@api.get("/questions",name = "Retourne tout les questions disponible",
          responses ={200: {"description": "OK"},
                      401 : {"description":"User password incorrect"},
                      409: {"description": "No allow to add question"}},
          tags=['question','admin'] )
async def get_all_question(Authorization:str = Header()) -> list[Question]:
    """""Fonction permettant a un admin de voir toutes les questions disponible """""
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
                      409: {"description": "No allow to add question"}},
          tags=['question','admin'] )
async def create_question(question: Question,Authorization:str = Header()):
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


@api.get("/questions/use",name = "Retourne tout les questions disponible pour un use donnée",
          responses ={200: {"description": "OK"},
                      401 : {"description":"User password incorrect"},
                      406: {"description": "Not enougth questions " }},
          tags=['question'] )
async def get_qcm_by_use(request_use:Request_Use,Authorization:str = Header())-> list[Question]:
    """Retourne tout les questions disponible pour un use donnée"""
    user,password = Authorization.split(':')
    if not check_usrpwd(user,password):
        raise  HTTPException(status_code=401,detail=f"User password incorrect ")
    try:
        result = base_de_donnee[base_de_donnee.use == request_use.use ].sample(request_use.nb_question).to_json(orient='records')
    except ValueError:
        raise  HTTPException(status_code=406,detail=f"Request too restrictive to raise {request_use.nb_question} questions")
    return json.loads(result) 


@api.get("/questions/subjects",name = "Retourne tout les questions disponible pour un liste de sujet donnée",
          responses ={200: {"description": "OK"},
                      401 : {"description":"User password incorrect"},
                      406: {"description": "Not enougth questions " }},
          tags=['question','admin'] )

async def get_qcm_by_subjects(resquest_subjects: Request_Subjects ,Authorization:str = Header())-> list[Question]:
    """Retourne tout les questions disponible pour un liste de sujet donnée"""
    user,password = Authorization.split(':')
    if not check_usrpwd(user,password):

        raise  HTTPException(status_code=401,detail=f"User password incorrect")
    try:
        result = base_de_donnee[base_de_donnee.subject.isin(resquest_subjects.subjects )].sample(resquest_subjects.nb_question).to_json(orient='records')
    except ValueError:
        raise  HTTPException(status_code=406,detail=f"Request too restrictive to raise {resquest_subjects.nb_question} questions")
    return json.loads(result) 
   
