FROM python:3.9

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR .

RUN apt-get -y update
RUN apt-get install chromium -y
RUN apt-get -y upgrade
RUN apt install apt-utils

COPY . .
RUN pip install -r requirements.txt
RUN chmod +x drivers/chromedriver_90_x
