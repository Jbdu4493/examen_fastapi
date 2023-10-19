#/bin/bash
pip install --upgrade pip
pip install -r requirements.txt
sudo apt-get install uvicorn &
uvicorn main:api --reload &