FROM python:3.12.4-slim

WORKDIR /usr/src/chat/src

ENV PYTHONPATH=/usr/src/chat/src

COPY /requirements/base.txt /requirements/

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r /requirements/base.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
