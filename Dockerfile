FROM ubuntu:18.04
MAINTAINER fnndsc "kirch@upwork.com"

ENV DEBIAN_FRONTEND=noninteractive

COPY . /app/

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && apt-get install -y default-libmysqlclient-dev build-essential \
  && apt-get install -y poppler-utils \
  && cd /app \
  && pip install -r requirements.txt \
  && python backend/manage.py makemigrations \
  && python backend/manage.py migrate main \
  && python backend/manage.py migrate social_django \
  && python backend/manage.py migrate \
