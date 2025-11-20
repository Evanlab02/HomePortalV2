.PHONY: install
install:
	@echo "⚙️ Creating local compose..."
	@cp compose.prod.yml compose.yml
	@echo "ℹ️ Your compose file: compose.yml"
	@echo "✅ Created local compose"
	@echo ""
	@echo "⚙️ Creating compose modules..."
	@cp modules/actual/compose.ext.yml modules/actual/compose.yml
	@cp modules/dns/compose.ext.yml modules/dns/compose.yml
	@cp modules/files/compose.ext.yml modules/files/compose.yml
	@cp modules/flame/compose.ext.yml modules/flame/compose.yml
	@cp modules/immich/compose.ext.yml modules/immich/compose.yml
	@cp modules/pgadmin/compose.ext.yml modules/pgadmin/compose.yml
	@cp modules/servarr/compose.ext.yml modules/servarr/compose.yml
	@cp modules/yacht/compose.ext.yml modules/yacht/compose.yml
	@echo "✅ Created compose modules"
	@echo ""
	@echo "⚙️ Creating local Caddyfiles"
	@cp conf/live/Caddyfile conf/custom/Caddyfile
	@echo "ℹ️ Your primary Caddyfile: conf/custom/Caddyfile"
	@cp conf/maintenance/Caddyfile conf/custom/maintenance/Caddyfile
	@echo "ℹ️ Your maintenance Caddyfile: conf/custom/maintenance/Caddyfile"
	@echo "✅ Created Caddyfiles"
	@echo ""
	@echo "⚙️ Creating .env files off of template"
	@cp .env.template .env
	@echo "ℹ️ Your primary env file: .env"
	@cp modules/dns/.env.template modules/dns/.env
	@echo "ℹ️ Your Pihole/DNS env file: modules/dns/.env"
	@cp modules/flame/.env.template modules/flame/.env
	@echo "ℹ️ Your Flame env file: modules/flame/.env"
	@cp modules/immich/.env.template modules/immich/.env
	@echo "ℹ️ Your Immich env file: modules/immich/.env"
	@cp modules/pgadmin/.env.template modules/pgadmin/.env
	@echo "ℹ️ Your PgAdmin env file: modules/pgadmin/.env"
	@cp modules/servarr/.env.template modules/servarr/.env
	@echo "ℹ️ Your Servarr env file: modules/servarr/.env"
	@echo "✅ Created .env files"
	@echo ""
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
	@echo "⚙️ Generating passwords for modules/immich/.env"
	@sed -i "s|^IMMICH_DB_PASSWORD=.*|IMMICH_DB_PASSWORD=$$(openssl rand -base64 32)|" modules/immich/.env
	@echo "⚙️ Generating passwords for modules/pgadmin/.env"
	@sed -i "s|^PGADMIN_DEFAULT_PASSWORD=.*|PGADMIN_DEFAULT_PASSWORD=$$(openssl rand -base64 32)|" modules/pgadmin/.env
	@echo "⚙️ Generating passwords for modules/servarr/.env"
	@sed -i "s|^TUBESYNC_PW=.*|TUBESYNC_PW=$$(openssl rand -base64 32)|" modules/servarr/.env
	@echo "✅ Generated passwords"
	@echo ""
	@echo ""
	@echo "📢 IMPORTANT INFORMATION BELOW 📢"
	@echo "========================================================================================================================"
	@echo ""
	@echo "----------------------------------------------- ENV VARS ---------------------------------------------------------------"
	@echo ""
	@echo "📢 You need to fill in anything in the .env file that is blank and required. Not all values are populated by default."
	@echo "📢 Here is a list of env vars you will likely need to update:"
	@echo "📢 ==> DJANGO_HOSTS : Comma seperated list of the hosts the main portal app will be available at, eg. app.example.com"
	@echo "📢 ==> DJANGO_CLOUDFLARE_API_KEY : The cloudflare API key to be used for the cloudflare integration."
	@echo "📢 ==> AUTHENTIK_AUTHENTIK__EXTERNAL_HOST : eg. auth.example.com"
	@echo "📢 ==> AUTHENTIK_BOOTSTRAP_EMAIL : eg. example@gmail.com"
	@echo "📢 ==> PGADMIN_DEFAULT_EMAIL (modules/pgadmin/.env) : eg. example@gmail.com"
	@echo "📢 ==> WIREGUARD_PRIVATE_KEY (modules/servarr/.env) : Key from ProtonVPN"
	@echo ""
	@echo "----------------------------------------- DOMAIN CONFIGURATION ----------------------------------------------------------"
	@echo ""
	@echo "📢 You need to configure the caddyfile to point to the correct domains for all your applications. We assume that you"
	@echo "📢 know how to configure your DNS."
	@echo ""
	@echo "--------------------------------------------- CERTIFICATES -------------------------------------------------------------"
	@echo ""
	@echo "📢 Remember there is a guide to getting certs setup for private networks/IPs"
	@echo "📢 Ensure your Caddyfile matches to what your cert files look like."
	@echo ""
	@echo "----------------------------------------------- MODULES ----------------------------------------------------------------"
	@echo ""
	@echo "📢 Please ensure you comment out 'modules' that you will not be using in the compose.yml file under the include"
	@echo "📢 statement. These 'modules' are optional and are not core functionality of home portal."
	@echo ""
	@echo "------------------------------------------------ VOLUMES ---------------------------------------------------------------"
	@echo ""
	@echo "📢 Configure your volumes to point to the location you want your data to be stored. Here are the volumes that will not"
	@echo "📢 Be automatically configured and require intervention:"
	@echo "📢 ==> modules/immich/compose.yml --> Look for text '- SETTOLOCATION:/usr/src/app/upload' (Line 22 +-)"
	@echo "📢 ==> modules/servarr/compose.yml --> Look for all locations that have 'SETTOLOCATION' for volume config"
	@echo ""
	@echo "========================================================================================================================"

.PHONY: superuser
superuser:
	docker compose exec admin python manage.py createsuperuser
