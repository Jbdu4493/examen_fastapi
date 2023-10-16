from typing import Optional, List,Dict
from sqlmodel import Field,SQLModel,create_engine,select,Session
import random
class Question(SQLModel,table=True):
    """Modélisation d'un question disponible dans l'application"""
    id: Optional[int] = Field(default=None, primary_key=True,index=True)
    question : str
    use : str
    correct : List[str]
    responseA : str
    responseB : str
    responseC : str
    responseD : Optional[str] = None
    remark : Optional[str] = None

class User(SQLModel,table=True):
    """Modélisation d'un user disponible dans l'application"""
    user_name: None #Field(default=None, primary_key=True,index=True)
    user_password: str
    admin: bool


class UserPasswordException(Exception):
    pass

class UserNotExistException(Exception):
    pass

class UserNotAdmin(Exception):
    pass

class Controleur:

    def __init__(self,database_name):
        sqlite_url = f"sqlite:///{database_name}"
        self.engine = create_engine(sqlite_url, echo=True)
        SQLModel.metadata.create_all(self.engine)



    def is_admin(self, user_name: str) -> bool:
        with Session(self.engine) as session:
            statement = select(User).where(User.user_name == user_name )
            results = session.exec(statement)
        return results[0].admin
    
    def check_user_password(self, user_name: str,user_password: str):
        with Session(self.engine) as session:
            statement = select(User).where(User.user_name == user_name )
            results = session.exec(statement)
            if len(results) == 0:
                raise UserNotExistException(f"L'utilisateur {user_name} exite pas pas")
            else:
                statement = select(User).where(User.user_name == user_name and User.user_password == user_password )
                results = session.exec(statement)
                if len(results) == 0:
                    raise UserPasswordException(f"L'utilisateur {user_name} exite pas pas")
                return "OK"
            
    def add_user(self, user_name: str,user_password: str, user: User):
        self.check_user_password(user_name,user_password)
        if self.is_admin(user_name):
            with Session(self.engine) as session:
                session.add(user)
                session.commit()

    def add_question(self, user_name: str,user_password: str, question:Question):
        self.check_user_password(user_name,user_password)
        if self.is_admin(user_name):
            with Session(self.engine) as session:
                session.add(question)
                session.commit()
    
    def delete_user(self, user_name: str,user_password: str, user_name_to_del:str):
        self.check_user_password(user_name,user_password)
        if self.is_admin(user_name):
            with Session(self.engine) as session:
                statement = select(User).where(User.user_name == user_name_to_del)
                results = session.exec(statement)
                user = results.one()

                session.delete(user)
                session.commit()

    def delete_question(self, user_name: str,user_password: str , id:int):
        self.check_user_password(user_name,user_password)
        if self.is_admin(user_name):
            with Session(self.engine) as session:
                statement = select(Question).where(Question.id == id)
                results = session.exec(statement)
                question = results.one()

                session.delete(question)
                session.commit()
    
    def get_all_users(self, user_name: str,user_password: str ) -> List[User]:
        self.check_user_password(user_name,user_password)
        if self.is_admin(user_name):
            with Session(self.engine) as session:
                statement = select(User)
                results = session.exec(statement)
            return results

    def get_all_users(self, user_name: str,user_password: str ) -> List[Question]:
        self.check_user_password(user_name,user_password)
        if self.is_admin(user_name):
            with Session(self.engine) as session:
                statement = select(Question)
                results = session.exec(statement)
            return results


    def get_questions_by_use(self, user_name: str,user_password: str, use:str, nb_question:int):
        self.check_user_password(user_name,user_password)
        with Session(self.engine) as session:
            statement = select(Question).where(Question.use == use)
            results = session.exec(statement)
        return random.sample(results,nb_question)



    def get_questions_by_subject(self, user_name: str,user_password: str, subject: List[str], nb_question: int):
        self.check_user_password(user_name,user_password)
        with Session(self.engine) as session:
            statement = select(Question).where(Question.use in subject)
            results = session.exec(statement)
        return random.sample(results,nb_question)