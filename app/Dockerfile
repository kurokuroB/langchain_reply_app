FROM python:3.10-buster

WORKDIR /app
ADD . /app

RUN apt-get update && apt-get clean
RUN pip install --upgrade pip
RUN pip install -r requirements.txt