import streamlit as st
import requests
import pandas as pd
import json

# Initialise le volet gauche
st.sidebar.title("Connexion")

username = st.sidebar.text_input("Nom d'utilisateur",value="admin")
password = st.sidebar.text_input("Mot de passe",value='4dm1N' ,type="password")
ip_server = st.sidebar.text_input("adresse IP du server de API",value='localhost')
tab1, tab2, tab3,tab4,tab5,tab6,tab7 = st.tabs(['**Introduction**',
                              "**Voir les questions**",
                              "**Créer question**",
                              "**Générer un qcm par use**",
                              "**Générer un qcm par sujet**",
                               "**Voir les utilisateurs**",
                                "**Créer un utilisateur**",
                              ])


with tab1:
    st.markdown(""" ### Présentation

-   Chaque onglet correspond a un fonctionnalité fourni par l'api 
-   <- 2 mot de passe sont a saisir user/pwd ("admin", "4dm1N") et ("joe","biz") 
- [Lien OPENAPI](http://127.0.0.1:8000/docs)
 ### Authantification
L'utilisateur  et mot de passe sera passer via le header ***Authorization*** .

""") 

with tab2:
    st.markdown("""### Curl 
""") 
    txt = st.text_area("Commande","""curl -X 'GET' 'http://localhost:8000/questions' 
  -H 'accept: application/json' 
  -H 'Authorization: admin:4dm1N'""")
    st.markdown(""" ### Resultat de la requête""")
    if st.button("Toutes les questions "):
    
        response = requests.get(f"http://{ip_server}:8000/questions",headers={"accept":"application//json","Authorization":f"{username}:{password}"})
        if response.status_code ==200:
            result =  response.json()
            df = pd.DataFrame(result)
            st.dataframe(df)
        else:
            detail = response.json().get('detail','')
            st.error(f"{response.status_code} {detail}")   
        
with tab3:
    st.markdown("""    ### Curl """) 
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
        response = requests.post(url=f"http://{ip_server}:8000/questions",
                                headers={"accept":"application//json",
                                         'Content-Type': 'application/json',
                                        "Authorization":f"{username}:{password}"},
                                json = body_question )
        if response.status_code ==200:
            st.success('This is a success message!', icon="✅")
        else:
            detail = response.json().get('detail','')
            st.error(f"{response.status_code} {detail}") 

with tab4:
    
    st.markdown("""    ### Curl """) 
    txt = st.text_area("Commande",""" curl -X 'GET' 'http://localhost:8000/questions/use' 
-H 'accept: application/json'
-H 'Content-Type: application/json'
-H 'Authorization: joe:biz'
-d '{"subject":"Test de validation","nb_question":2}'""")
    
    st.markdown(""" ### Resultat de la requête""")
    response = requests.get(f"http://{ip_server}:8000/questions",headers={"accept":"application//json","Authorization":f"{username}:{password}"})

    if response.status_code ==200:
            result =  response.json()
            df = pd.DataFrame(result)
            uses = list(set(df.use))
    else:
        uses = list()

    text_nb_quest= st.text_input("Nombre de question",'4')
    selected_uses = st.selectbox(
    "Selectionné l'utilisation: ",
    uses)
    try:
        nb_ques = int(text_nb_quest)
    except ValueError:
        st.error('Le nombre de question doit etre un nombre entier pos', icon="🚨")



    if st.button("Requêter",key='req_use'):
        response = requests.get("http://{ip_server}:8000/questions/use",
                                headers={"accept":"application//json",
                                         "Authorization":f"{username}:{password}",
                                         'Content-Type': 'application/json'},
                                json={"use":selected_uses,"nb_question":nb_ques})
        if response.status_code ==200:
            result =  response.json()
            df = pd.DataFrame(result)
            st.dataframe(df)
        else:
            detail = response.json().get('detail','')
            st.error(f"{response.status_code} {detail}") 

with tab5:
    st.markdown("""    ### Curl """) 
    txt = st.text_area("Commande ",""" curl -X 'GET' 
  'http://localhost:8000/questions/subjects' 
  -H 'accept: application/json' 
  -H 'Content-Type: application/json' 
  -H 'Authorization: joe:biz'
  -d '{"subjects":["Data Science","Classification"],"nb_question":2}'""")
    
    st.markdown(""" ### Resultat de la requête""")
    response = requests.get(f"http://{ip_server}:8000/questions",headers={"accept":"application//json","Authorization":f"{username}:{password}"})
    subject = []
    if response.status_code ==200:
            result =  response.json()
            df = pd.DataFrame(result)
            subject = list(set(df.subject))

    txt_subject = st.text_area("Sujet possible", ','.join(subject))
    st.text("Effacer les sujets que vous ne souhaitez pas ou ajouter s'en avec les separateur ','")

    text_nb_quest= st.text_input("Nombre de question ",'4')
    all_subject= txt_subject.split(',')
    try:
        nb_ques = int(text_nb_quest)
    except ValueError:
        st.error('Le nombre de question doit etre un nombre entier pos', icon="🚨")



    if st.button("Requêter",key='req_subj'):
        response = requests.get(f"http://{ip_server}:8000/questions/subjects",
                                headers={"accept":"application//json",
                                         "Authorization":f"{username}:{password}",
                                         'Content-Type': 'application/json'},
                                json={"subjects":all_subject,"nb_question":nb_ques})
        if response.status_code ==200:
            
            result =  response.json()
            df = pd.DataFrame(result)
            st.dataframe(df)
        else:
            detail = response.json().get('detail','')
            st.error(f"{response.status_code} {detail}")

with tab6:
    st.markdown("""    ### Curl """) 
    txt = st.text_area("Commande ","""   curl -X 'GET' \
  'http://localhost:8000/users' 
  -H 'accept: application/json' 
  -H 'Authorization: admin:4dm1N' """)
    st.markdown(""" ### Resultat de la requête""")
    if st.button("Requêter",key='req_user'):
        response = requests.get(f"http://{ip_server}:8000/users",headers={"accept":"application//json","Authorization":f"{username}:{password}"})
    
        if response.status_code ==200:
            
            result =  response.json()
            user = result.keys()
            pwd = [result[u] for u in result]
            df = pd.DataFrame({"Utilisateur":user,"mot de pass":pwd})
            st.dataframe(df)
        else:
            detail = response.json().get('detail','')
            st.error(f"{response.status_code} {detail}")
with tab7: 
    st.markdown("""    ### Curl """) 
    txt = st.text_area("Commande ","""   curl -X 'GET' \
  'http://localhost:8000/users' 
  -H 'accept: application/json' 
  -H 'Authorization: admin:4dm1N'
  -d '{
    "user_name": "datascientest",
    "password": "1232134"
  }' """)
    text_username = st.text_input("Nom de l'utilisateur",key='username')
    text_password= st.text_input("Mot de passe",key='password')
    st.markdown(""" ### Tester de la requête""")
    if st.button("Requêter",key='req_user_add'):
        user1 = {"user_name": text_username,"password": text_password}
        response = requests.post(f"http://{ip_server}:8000/users",
                                headers={"accept":"application//json","Authorization":f"{username}:{password}"},
                                json = user1 )
    
        if response.status_code ==200:
            st.success("Utilisateur créer/modifier", icon="✅")
        else:
            detail = response.json().get('detail','')
            st.error(f"{response.status_code} {detail}") 
    