FROM python:3.7-slim-buster

RUN apt-get update && \
    apt-get install -y httpie build-essential swig netcat\
    less vim wget jq
RUN mkdir /app && chmod 777 /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Necessary because caching and faster builds
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app/
CMD ["gunicorn twitter.wsgi -b 0.0.0.0:8000 -w=10"]
