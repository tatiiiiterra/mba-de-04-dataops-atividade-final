# NOTE name need to be Dockerfile
FROM python:3.9

ARG db_user
ARG db_password

ENV DB_USER $db_user
ENV DB_PASSWORD $db_password

RUN mkdir -p /usr/src/python-app/data/raw

WORKDIR /usr/src/python-app

COPY . /usr/src/python-app/

RUN pip install -r ./python/requirements.txt
