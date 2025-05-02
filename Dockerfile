FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl
RUN pip install poetry==1.8.5

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction

COPY src  .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]