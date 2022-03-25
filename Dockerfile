#Dockerfile 
# syntax=docker/dockerfile:1

FROM ubuntu:20.04

LABEL maintainer="Rodrigo Pereira"

COPY . .

RUN apt-get update 

RUN apt-get install pip -y 

RUN pip install -r requirements.txt

RUN export FLASK="main.py"

CMD ["python3", "main.py"]