.PHONY: pull
pull:
	docker compose pull

.PHONY: build
build:
	docker compose build

.PHONY: up
up:
	docker compose up

.PHONY: down
down:
	docker compose down

.PHONY: refresh
refresh:
	docker compose up --build

.PHONY: dev
dev:
	docker compose watch

.PHONY: caddy-fmt
caddy-fmt:
	docker run --rm -v `pwd`/Caddyfile:/etc/caddy/Caddyfile caddy:2.10.2-alpine caddy fmt /etc/caddy/Caddyfile --overwrite

.PHONY: staging
staging:
	docker compose -f compose.staging.yaml pull
	docker compose -f compose.staging.yaml build
	docker compose -f compose.staging.yaml up

.PHONY: staging-down
staging-down:
	docker compose -f compose.staging.yaml down

.PHONY: prod
prod:
	docker compose -f compose.prod.yaml pull
	docker compose -f compose.prod.yaml build
	docker compose -f compose.prod.yaml up

.PHONY: prod-down
prod-down:
	docker compose -f compose.prod.yaml down
