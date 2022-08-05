FROM python:3.10.5

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt-get install -y chromium
RUN apt-get install -y chromium-driver

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

