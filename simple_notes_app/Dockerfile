FROM python:3.11-slim

WORKDIR /app


RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root

COPY . .

EXPOSE 8000

