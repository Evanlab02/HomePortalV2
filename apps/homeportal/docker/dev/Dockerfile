FROM python:3.13.9-alpine3.22

LABEL org.opencontainers.image.title="Home Portal V2 API/ADMIN - Development"
LABEL org.opencontainers.image.version="DEV"
LABEL org.opencontainers.image.licenses="MIT"

EXPOSE 8000

RUN apk add --no-cache bash

ENV UV_SYSTEM_PYTHON=1
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN uv pip install -r requirements.txt

COPY ./manage.py ./manage.py
COPY ./api ./api
COPY ./app ./app
COPY ./utils ./utils

ENTRYPOINT [ "python", "manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]
