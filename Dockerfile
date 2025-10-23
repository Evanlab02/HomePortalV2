FROM python:3.14.0-alpine3.22 AS docs

ENV UV_SYSTEM_PYTHON=1
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/
WORKDIR /build
COPY ./documentation/requirements.txt ./requirements.txt
RUN uv pip install -r requirements.txt
COPY ./documentation/docs ./docs/
COPY ./documentation/mkdocs.yml ./mkdocs.yml
RUN mkdocs build

FROM caddy:2.10.2-alpine AS final

LABEL org.opencontainers.image.title="Home Portal V2 Caddy - Development"
LABEL org.opencontainers.image.version="DEV"
LABEL org.opencontainers.image.licenses="MIT"

EXPOSE 80 443

RUN apk add --no-cache bash

COPY --from=docs /build/site /var/www/html/docs/
COPY Caddyfile /etc/caddy/Caddyfile
