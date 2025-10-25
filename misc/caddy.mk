.PHONY: caddy-fmt
caddy-fmt:
	docker run --rm -v `pwd`/conf/maintenance/Caddyfile:/etc/caddy/Caddyfile caddy:2.10.2-alpine caddy fmt /etc/caddy/Caddyfile --overwrite
	docker run --rm -v `pwd`/conf/release/Caddyfile:/etc/caddy/Caddyfile caddy:2.10.2-alpine caddy fmt /etc/caddy/Caddyfile --overwrite
