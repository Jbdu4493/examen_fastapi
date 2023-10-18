import streamlit as st
import requests
import pandas as pd
import json

# Initialise le volet gauche
st.sidebar.title("Connexion")

username = st.sidebar.text_input("Nom d'utilisateur",value="admin")
password = st.sidebar.text_input("Mot de passe",value='4dm1N' ,type="password")

tab1, tab2, tab3,tab4,tab5 = st.tabs(['**Introduction**',
                              "**Tout les question**",
                              "**Creation**",
                              "**Question par use**",
                              "**Question par suject**"
                              ])


with tab1:
    st.markdown(""" ### Présentation

-   Chaque onglet correspond a un fonctionnalité fourni par l'api 
-   <- 2 mot de passe sont a saisir user/pwd ("admin", "4dm1N") et ("joe","biz") 
- [Lien OPENAPI](http://127.0.0.1:8000/docs) 
""") 
with tab2:
    st.markdown(""" ### Toutes les question
Cette fonctionnalite est disponible uniquement pour l'admin user. Le user mote de passe sera passer via le header ***Authorization***.

### Curl 
""") 
    txt = st.text_area("Commande","""curl -X 'GET' 'http://localhost:8000/questions' 
  -H 'accept: application/json' 
  -H 'Authorization: admin:4dm1N'""")
    st.markdown(""" ### Resultat de la requête""")
    if st.button("Toutes les questions "):
    
        response = requests.get("http://localhost:8000/questions",headers={"accept":"application//json","Authorization":f"{username}:{password}"})
        
        result =  response.json()
        df = pd.DataFrame(result)
        st.dataframe(df)
with tab3:
    st.markdown(""" ### Ajout d'une question
    L'ajout de question de fait par un méthode ***POST*** et la questions à rajouter est dans le body de la requete.

    ### Curl 
""") 
    txt = st.text_area("Commande","""  curl -X 'POST' 
    'http://localhost:8000/questions' 
    -H 'accept: application/json' 
    -H 'Content-Type: application/json' 
    -d '{"question": "Quelle est le meilleur instutue de formation en Data",
    "subject": "Sondage",
    "use": "Formation",
    "correct": ["A"],
    "responseA": "DataScientest.com",
    "responseB": "Le wagon",
    "responseC": "OpenClassroom",
    "responseD": null,
    "remark": null}""")
    st.markdown(""" ### Tester la requête d'ajout """)
    text_question = st.text_input("Question")
    text_use = st.text_input("use")
    text_subject = st.text_input("Subject")
    text_responseA= st.text_input("Response A")
    text_responseB = st.text_input("Response B")
    text_responseC = st.text_input("Response C")
    text_responseD = st.text_input("Response D")
    text_remark = st.text_input("Remark")
    correct = list()
    
    st.markdown("Reponse Correct:")
    repA = st.checkbox('A')
    if repA:
        correct.append("A")
    repB = st.checkbox('B')
    if repB:
        correct.append("B")
    repC  = st.checkbox('C')
    if repC:
        correct.append("C")
    repD = st.checkbox('D')
    if repD:
        correct.append("D")


    body_question = {"question":text_question if text_question != "" else None ,
    "subject":text_subject if text_subject != "" else None ,
    "use": text_use if text_use != "" else None,
    "correct": correct ,
    "responseA": text_responseA if text_responseA != "" else None,
    "responseB": text_responseB if text_responseB != "" else None,
    "responseC": text_responseC if text_responseC != "" else None,
    "responseD": text_responseD if text_responseD != "" else None,
    "remark": text_remark if text_remark !=  "" else None }
    if st.button("Ajouter question"):
        response = requests.post(url="http://localhost:8000/questions",
                                headers={"accept":"application//json",
                                         'Content-Type': 'application/json',
                                        "Authorization":f"{username}:{password}"},
                                json = body_question )
        
        