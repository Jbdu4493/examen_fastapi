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
  -d '{"question": "string",
  "subject": "string",
  "use": "string",
  "correct": ["string"],
  "responseA": "string",
  "responseB": "string",
  "responseC": "string",
  "responseD": "string",
  "remark": "string"}'
echo -e '\n  ---------------------------- \n'
  curl -X 'GET' \
  'http://localhost:8000/questions' \
  -H 'accept: application/json' \
  -H 'Authorization: admin:4dm1N'
echo -e '\n  ---------------------------- \n'

curl -X 'GET' \
  'http://localhost:8000/questions/use?use=Test%20de%20validation&nb_question=20' \
    -H 'accept: application/json' \
    -H 'Authorization: admin:4dm1N'

curl -X 'GET' \
  'http://localhost:8000/questions/subjects?nb_question=4' \
  -H 'accept: application/json' \
  -H 'Authorization: joe:biz' \
  -d '["Data Science","Classification"]'
