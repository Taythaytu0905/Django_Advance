FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app
COPY . /app/

COPY requirements.txt /app/
RUN pip install -r requirements.txt

RUN adduser -D user
USER user