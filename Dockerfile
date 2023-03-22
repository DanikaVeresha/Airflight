FROM python:3.10

WORKDIR /rate_manage

COPY requirements.txt requirements.txt
RUN /bin/sh -c pip3 install -r requirements.txt]

COPY . .


