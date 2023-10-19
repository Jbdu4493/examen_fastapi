#/bin/bash
pip install --upgrade pip
pip3 install httptools==0.1.* uvloop, streamlit
pip install -r requirements.txt
sudo apt-get install uvicorn &
uvicorn main:api --reload &