FROM ubuntu:20.04
RUN apt-get update && apt-get install python3-pip -y 
ADD streamlit_test_api.py /sources/
WORKDIR /sources/
RUN pip3 install streamlit
CMD streamlit run streamlit_test_api.py --server.port 7000
