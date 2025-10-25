.PHONY: pull
pull:
	docker compose pull

.PHONY: build
build:
	docker compose build

.PHONY: up
up:
	docker compose up -d

.PHONY: down
down:
	docker compose down

.PHONY: refresh
refresh:
	docker compose up --build

.PHONY: debug
debug:
	docker compose up -d

.PHONY: maintenance
maintenance:
	docker compose -f compose.maintenance.yml pull
	docker compose -f compose.maintenance.yml build
	docker compose -f compose.maintenance.yml up

.PHONY: maintenance-down
maintenance-down:
	docker compose -f compose.maintenance.yml down
