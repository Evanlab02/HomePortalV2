# Unified Dockerfile for all Home Portal V2 services
# Build specific services using --target flag:
#   docker build --target admin -t homeportal-admin:latest .
#   docker build --target app -t homeportal-app:latest .
#   docker build --target queue -t homeportal-queue:latest .

# ==============================================================================
# Base stage - shared across all services
# All services will inherit these exact same layers with identical hashes
# ==============================================================================
FROM python:3.13.9-alpine3.22 AS base

LABEL org.opencontainers.image.licenses="MIT"

ENV UV_SYSTEM_PYTHON=1

RUN apk add --no-cache bash

COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN uv pip install -r requirements.txt

COPY ./api ./api
COPY ./app ./app
COPY ./cloudflare ./cloudflare
COPY ./qbit ./qbit
COPY ./utils ./utils

# ==============================================================================
# Admin service
# ==============================================================================
FROM base AS admin

LABEL org.opencontainers.image.title="Home Portal V2 ADMIN"
LABEL org.opencontainers.image.version="LIVE"

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=app.settings.admin.settings

COPY ./manage.py ./manage.py
COPY ./scripts/admin.start.sh ./admin.start.sh
RUN chmod +x /app/admin.start.sh

ENTRYPOINT [ "sh", "./admin.start.sh" ]

# ==============================================================================
# App service
# ==============================================================================
FROM base AS app

LABEL org.opencontainers.image.title="Home Portal V2 APP"
LABEL org.opencontainers.image.version="LIVE"

EXPOSE 8000

ARG WORKERS=1
ENV DJANGO_GUNICORN_WORKERS=${WORKERS}
ENV DJANGO_SETTINGS_MODULE=app.settings.core.settings

COPY ./scripts/server.start.sh ./server.start.sh
RUN chmod +x /app/server.start.sh

ENTRYPOINT [ "sh", "./server.start.sh" ]

# ==============================================================================
# Queue/Worker service
# ==============================================================================
FROM base AS queue

LABEL org.opencontainers.image.title="Home Portal V2 WORKER"
LABEL org.opencontainers.image.version="LIVE"

ENV DJANGO_SETTINGS_MODULE=app.settings.core.settings
COPY ./scripts/queue.start.sh ./queue.start.sh
RUN chmod +x /app/queue.start.sh

ENTRYPOINT [ "sh", "./queue.start.sh" ]
