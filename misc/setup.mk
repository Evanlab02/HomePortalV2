.PHONY: env
env:
	@echo "⚙️ Creating local compose..."
	@cp compose.prod.yml compose.yml
	@echo "ℹ️ Your compose file: compose.yml"
	@echo "✅ Created local compose"

	@echo "⚙️ Creating local Caddyfiles"
	@cp conf/live/Caddyfile conf/custom/Caddyfile
	@echo "ℹ️ Your primary Caddyfile: conf/custom/Caddyfile"
	@cp conf/maintenance/Caddyfile conf/custom/maintenance/Caddyfile
	@echo "ℹ️ Your maintenance Caddyfile: conf/custom/maintenance/Caddyfile"
	@echo "✅ Created Caddyfiles"

	@echo "⚙️ Creating .env files off of template"
	@cp .env.template .env
	@echo "ℹ️ Your primary env file: .env"
	@cp modules/dns/.env.template modules/dns/.env
	@echo "ℹ️ Your Pihole/DNS env file: modules/dns/.env"
	@cp modules/flame/.env.template modules/flame/.env
	@echo "ℹ️ Your Flame env file: modules/flame/.env"
	@echo "✅ Created .env files"

	@echo "⚙️ Generating passwords (But you are welcome to change them)"
	@echo "⚙️ Generating passwords for .env"
	@sed -i "s|^DJANGO_SECRET_KEY=.*|DJANGO_SECRET_KEY=$$(openssl rand -base64 32)|" .env
	@sed -i "s|^DJANGO_DB_PASSWORD=.*|DJANGO_DB_PASSWORD=$$(openssl rand -base64 32)|" .env
	@sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=$$(openssl rand -base64 32)|" .env
	@sed -i "s|^AUTHENTIK_SECRET_KEY=.*|AUTHENTIK_SECRET_KEY=$$(openssl rand -base64 32)|" .env
	@sed -i "s|^AUTHENTIK_POSTGRESQL__PASSWORD=.*|AUTHENTIK_POSTGRESQL__PASSWORD=$$(openssl rand -base64 32)|" .env
	@sed -i "s|^AUTHENTIK_BOOTSTRAP_PASSWORD=.*|AUTHENTIK_BOOTSTRAP_PASSWORD=$$(openssl rand -base64 32)|" .env
	@sed -i "s|^AUTHENTIK_BOOTSTRAP_TOKEN=.*|AUTHENTIK_BOOTSTRAP_TOKEN=$$(openssl rand -base64 32)|" .env
	@echo "⚙️ Generating passwords for modules/dns/.env"
	@sed -i "s|^PIHOLE_PASSWORD=.*|PIHOLE_PASSWORD=$$(openssl rand -base64 32)|" modules/dns/.env
	@echo "⚙️ Generating passwords for modules/flame/.env"
	@sed -i "s|^PASSWORD=.*|PASSWORD=$$(openssl rand -base64 32)|" modules/flame/.env
	@echo "✅ Generated passwords"

	@echo ""
	@echo "📢 IMPORTANT INFORMATION BELOW 📢"
	@echo "========================================================================================================================"
	@echo ""
	@echo "📢 You need to fill in anything in the .env file that is blank and required. Not all values are populated by default."
	@echo "📢 Here is a list of env vars you will likely need to update:"
	@echo "📢 --> DJANGO_HOSTS : Comma seperated list of the hosts the main portal app will be available at, eg. app.example.com"
	@echo "📢 --> AUTHENTIK_AUTHENTIK__EXTERNAL_HOST : eg. auth.example.com"
	@echo "📢 --> AUTHENTIK_BOOTSTRAP_EMAIL : eg. example@gmail.com"
	@echo ""
	@echo "------------------------------------------------------------------------------------------------------------------------"
	@echo ""
	@echo "📢 You need to configure the caddyfile to point to the correct domains for all your applications. We assume that you"
	@echo "📢 know how to configure your DNS." Also ensure your jellyfin proxy is setup correctly as this can vary quite a bit"
	@echo "📢 depending on your setup."
	@echo ""
	@echo "------------------------------------------------------------------------------------------------------------------------"
	@echo ""
	@echo "📢 Remember that if runnning on a private network like tailscale, there is a guide to getting certs setup as automatic"
	@echo "📢 certificates from caddy will not work. The default Caddyfiles assume you will be providing certificates so adjust as"
	@echo "📢 needs be."
	@echo ""
	@echo "------------------------------------------------------------------------------------------------------------------------"
	@echo ""
	@echo "📢 Please ensure you comment out 'modules' that you will not be using in the compose.yml file under the include"
	@echo "📢 statements. These 'modules' are optional and are not core functionality of home portal."
	@echo ""
	@echo "========================================================================================================================"

.PHONY: superuser
superuser:
	docker compose exec admin python manage.py createsuperuser