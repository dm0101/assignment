FROM python:3

ENV PYTHONUNBUFFERRED 1

WORKDIR /code

ADD . /code

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /code