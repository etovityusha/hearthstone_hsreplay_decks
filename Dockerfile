FROM python:3.9

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR .

RUN apt-get -y update
RUN apt-get -y upgrade

COPY . .

RUN apt-get install -y chromium
RUN apt-get install -y chromium-driver

RUN pip install -r requirements.txt
