# Dockerfile
FROM python:3
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        mysql-client mysql-server libmariadb-dev default-libmysqlclient-dev
WORKDIR /usr/src/app
ADD config/requirements.txt ./
RUN pip3 install --upgrade pip; \
    pip3 install -r requirements.txt
RUN django-admin startproject myproject .; \
    mv ./myproject ./origproject