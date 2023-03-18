FROM python:3.10

WORKDIR /rate_manage

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

