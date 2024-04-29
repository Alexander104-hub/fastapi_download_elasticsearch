FROM python:3.8-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /fastapi_app
WORKDIR /fastapi_app

ENV FLASK_ENV=development

# CMD uvicorn app:app --reload --port=5000 --host=0.0.0.0