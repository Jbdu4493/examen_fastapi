#/bin/bash

python3 -m venv venv_examen_fastapi
source ./venv_examen_fastapi/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

sudo apt-get install uvicorn

uvicorn main:api --reload &git 
streamlit run st_test_api.py &