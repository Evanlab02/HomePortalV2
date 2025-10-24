FROM python:3.13.9-alpine3.22

LABEL org.opencontainers.image.title="Home Portal V2 ADMIN"
LABEL org.opencontainers.image.version="LIVE"
LABEL org.opencontainers.image.licenses="MIT"

EXPOSE 8000

ENV UV_SYSTEM_PYTHON=1
ENV DJANGO_SETTINGS_MODULE=app.admin.settings

RUN apk add --no-cache bash

COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN uv pip install -r requirements.txt

COPY ./manage.py ./manage.py
COPY ./api ./api
COPY ./app ./app
COPY ./utils ./utils
COPY ./scripts/server.start.sh ./server.start.sh

RUN chmod +x /app/admin.start.sh

ENTRYPOINT [ "sh", "./admin.start.sh" ]
