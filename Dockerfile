FROM python:3.11-bullseye

WORKDIR /libraryAPI
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
