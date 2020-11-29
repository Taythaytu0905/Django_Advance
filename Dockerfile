FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app
COPY . /app/

COPY requirements.txt /app/
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

RUN adduser -D user
USER user