.PHONY: delete-all-volumes
delete-all-volumes:
	docker volume rm hp_authentik-certs
	docker volume rm hp_authentik-media
	docker volume rm hp_authentik-templates
	docker volume rm hp_caddy-data
	docker volume rm hp_valkey-data
	docker volume rm hp_postgres-data
	docker volume rm hp_maintenance-data
