# syntax=docker/dockerfile:1.6

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "bluesea_app:create_app", "run", "--debug", "--host", "0.0.0.0", "--port", "5000"]
