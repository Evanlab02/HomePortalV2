FROM python:3.14.0-alpine3.22 AS docs

WORKDIR /build
ENV UV_SYSTEM_PYTHON=1
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/
COPY ./documentation/requirements.txt ./requirements.txt
RUN uv pip install -r requirements.txt
COPY ./documentation/docs ./docs/
COPY ./documentation/mkdocs.yml ./mkdocs.yml
RUN mkdocs build

FROM node:22.21.0-alpine3.22 AS maintenance

WORKDIR /build
COPY apps/maintenance/package.json ./package.json
COPY apps/maintenance/package-lock.json ./package-lock.json
RUN npm ci
COPY apps/maintenance/vite.config.js ./vite.config.js
COPY apps/maintenance/index.html ./index.html
COPY apps/maintenance/src ./src
RUN npm run build

FROM caddy:2.10.2-alpine AS final

LABEL org.opencontainers.image.title="Home Portal V2 Caddy"
LABEL org.opencontainers.image.version="LIVE"
LABEL org.opencontainers.image.licenses="MIT"

EXPOSE 80 443

RUN apk add --no-cache bash

COPY --from=docs /build/site /var/www/html/docs/
COPY --from=maintenance /build/dist /var/www/html/maintenance/
COPY conf/release/Caddyfile /etc/caddy/Caddyfile
COPY conf/maintenance/Caddyfile /etc/caddy/maintenance/Caddyfile

ENTRYPOINT [ "caddy" ]
CMD ["run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
