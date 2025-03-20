FROM python:3.12.3

RUN apt-get update && apt-get install -y nginx


COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY src/ /app/src
COPY config/ /app/config
COPY static/ /app/static
COPY tests/ /app/tests
COPY .env /app
COPY main.py /app
COPY pyproject.toml /app
COPY .flake8 /app


WORKDIR /app
