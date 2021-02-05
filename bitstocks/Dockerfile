FROM alpine:edge

RUN mkdir -p /usr/src/app 

RUN apk update && \
    apk add python3 python3-dev vim bash

COPY requirements.txt /usr/src/requirements.txt
RUN python3 -mensurepip
RUN python3 -mpip install -r /usr/src/requirements.txt

COPY project/ /usr/src/app/

WORKDIR /usr/src/app

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py test
