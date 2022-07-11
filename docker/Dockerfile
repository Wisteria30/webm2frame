FROM python:3.10-buster

RUN apt update && apt install tmux -y
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
