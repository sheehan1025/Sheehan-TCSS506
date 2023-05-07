FROM python:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#COPY app.py /usr/local/bin/app.py
#CMD app.py
