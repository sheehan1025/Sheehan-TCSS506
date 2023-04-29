FROM debian:buster-slim
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get -y install python3 python3-pip curl procps
Run pip3 install --upgrade pip && pip3 install flask
COPY hw_2.py /usr/local/bin/hw_2.py
CMD hw_2.py
