#Dockerfile 
# syntax=docker/dockerfile:1
FROM ubuntu:20.04

LABEL maintainer="Rodrigo Pereira"

WORKDIR /app
COPY . /app

RUN apt-get update 

RUN apt-get install pip -y 
RUN pip install fastapi 
RUN pip install pydantic 

RUN pip install -r requirements.txt

VOLUME ["/app"]

EXPOSE 8384

# Comando para rodar o servidor FastAPI usando uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8384"]