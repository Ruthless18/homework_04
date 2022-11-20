FROM python:3.10.8-bullseye

WORKDIR /var/data_base

RUN pip install --upgrade pip
RUN pip install poetry==1.2.2

COPY . .

RUN poetry install --only main