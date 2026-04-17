FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN addgroup --system app && adduser --system --ingroup app app \
 && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["gunicorn", "ProblemBuddy.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
