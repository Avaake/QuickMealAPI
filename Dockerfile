FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry==1.8.5

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction

COPY src .

RUN chmod +x prestart.sh

ENTRYPOINT ["./prestart.sh"]
