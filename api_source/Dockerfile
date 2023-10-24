FROM ubuntu:20.04
RUN apt-get update && apt-get install python3-pip -y 
ADD main.py /sources/
ADD requirements.txt /sources/
WORKDIR /sources/
RUN pip3 install -r requirements.txt
CMD uvicorn main:api  --host=0.0.0.0 --port 8000
