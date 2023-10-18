#/bin/bash

curl -X 'GET' \
  'http://localhost:8000/questions' \
  -H 'accept: application/json' \
  -H 'Authorization: admin:4dm1N'
echo -e '\n  ---------------------------- \n'
  curl -X 'GET' \
  'http://localhost:8000/questions' \
  -H 'accept: application/json' \
  -H 'Authorization: amin:4dm12'
echo -e '\n  ---------------------------- \n'
  curl -X 'POST' \
  'http://localhost:8000/questions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: admin:4dm1N'\
  -d '{"question": "Quelle est le meilleur instutue de formation en Data",
  "subject": "Sondage",
  "use": "Formation",
  "correct": ["D"],
  "responseA": "DataScientest.com",
  "responseB": "Le wagon",
  "responseC": "OpenClassroom",
  "responseD": null,
  "remark": null}'
echo -e '\n  ---------------------------- \n'
  curl -X 'GET' \
  'http://localhost:8000/questions' \
  -H 'accept: application/json' \
  -H 'Authorization: admin:4dm1N'
echo -e '\n  ---------------------------- \n'

curl -X 'GET' \
  'http://localhost:8000/questions/subjects' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: joe:biz'\
  -d '{"subjects":["Data Science","Classification"],"nb_question":2}'


curl -X 'GET' \
  'http://localhost:8000/questions/use' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: joe:biz'\
  -d '{"use":"Test de validation","nb_question":2}'


