FROM python:3.11-slim

RUN pip install poetry==1.8.5

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction

COPY src/.test.env /app/.test.env
COPY src  .