FROM ubuntu:20.04
RUN apt-get update && apt-get install python3-pip -y 
EXPOSE 8000
ADD main.py /sources/
ADD requirements.txt /sources/
WORKDIR /sources/
RUN pip3 install -r requirements.txt
CMD uvicorn main:api  --port 8000
