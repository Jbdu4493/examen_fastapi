import pytest
from sqlmodel import  create_engine,SQLModel
from controleur import Controleur, UserNotExistException,User,Question


# Créez une instance de la classe Controleur pour les tests
@pytest.fixture
def controleur_instance():
    return Controleur(":memory:")

# Créez une base de données SQLite temporaire
@pytest.fixture
def temp_database():

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.close()

# Test pour ajouter un utilisateur
def test_add_user(temp_database, controleur_instance):
    user = User(user_name="new_user", user_password="password", admin=True)
    controleur_instance.add_user("admin", "admin_password", user)


# Test pour ajouter une question
# def test_add_question(temp_database, controleur_instance):
#     question = Question(text="What is your question?", use="example_use")
#     controleur_instance.add_question("admin", "admin_password", question)

#     with Session(temp_database) as session:
#         question_in_db = session.get(Question, question.id)
#         assert question_in_db is not None

# # Test pour vérifier la validation du mot de passe de l'utilisateur
# def test_check_user_password(temp_database, controleur_instance):
#     with Session(temp_database) as session:
#         user = User(user_name="existing_user", user_password="password", admin=True)
#         session.add(user)
#         session.commit()

#         with pytest.raises(UserNotExistException):
#             controleur_instance.check_user_password("non_existant_user", "password")

#         with pytest.raises(UserPasswordException):
#             controleur_instance.check_user_password("existing_user", "wrong_password")
