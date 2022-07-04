# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1
COPY . .
CMD [ "python3", "main.py"]