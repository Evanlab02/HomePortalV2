# Installing Home Portal V2

IMPORTANT: DO NOT EXPOSE THIS TO THE PUBLIC. 

The home portal app stores values in plain text for some inter-application communication and will only be corrected in future. Do not under any circumstances allow public access as DB access or admin panel access will expose your application credentials. This is one reason why authentik exists as a another security layer but do not assume that this is secure enough.

## Pre-requisites

- Linux Distro
    - I recommend for the not so familiar with Linux, Debian or Ubuntu. I would put debian above ubuntu as it is more barebones allowing for you to set it up exactly as you want to but Ubuntu comes with some nice pre-defined defaults.
    - NOTE: Some documentation links to debian installation guides, these should be almost identical to Ubuntu but be sure to follow ubuntu instructions if there is a distinction.
    - Mac and Windows are not supported, this includes WSL. 
    - WSL is not supported.
- [Docker](https://docs.docker.com/engine/install/debian/)
- [Docker Compose](https://docs.docker.com/engine/install/debian/)
- [Tailscale](./dependencies/tailscale.md)
- [Cloudflare Managed Domain](./dependencies/cloudflare.md)
- [acme.sh](./dependencies/acme.md)

NOTE: All of the above is required and you should read the documentation relating to it.

## Installation

**NOTE: Home Portal V2 is still very early in development, so use with caution and pull with caution. It is not designed to run on just any configuration just yet so keep that in mind.**

Feel free to fork the repo and then clone it to your local as you might want to make some changes and adjust it to your liking as this is really probably best as a starting point for you to setup your home server instead of a guideline.

Otherwise just clone the repo as is and ensure to git pull every now and then for the latest updates.

```bash
git clone https://github.com/Evanlab02/HomePortalV2.git
```

### Disclaimer

If using the servarr compose module after going through the next steps, note that gluetun is configured to be used with ProtonVPN. If you would like to configure it for other VPN providers you will have to set this up manually.

### Env Command

To setup your environment so you can start configuring the portal to your needs, you will need to run the following Makefile command:

```bash
make env
```

The output will look something like the following:

```plaintext
⚙️ Creating local compose...
ℹ️ Your compose file: compose.yml
✅ Created local compose

⚙️ Creating compose modules...
✅ Created compose modules

⚙️ Creating local Caddyfiles
ℹ️ Your primary Caddyfile: conf/custom/Caddyfile
ℹ️ Your maintenance Caddyfile: conf/custom/maintenance/Caddyfile
✅ Created Caddyfiles

⚙️ Creating .env files off of template
ℹ️ Your primary env file: .env
ℹ️ Your Pihole/DNS env file: modules/dns/.env
ℹ️ Your Flame env file: modules/flame/.env
ℹ️ Your Immich env file: modules/immich/.env
ℹ️ Your PgAdmin env file: modules/pgadmin/.env
ℹ️ Your Servarr env file: modules/servarr/.env
✅ Created .env files

⚙️ Generating passwords (But you are welcome to change them)
⚙️ Generating passwords for .env
⚙️ Generating passwords for modules/dns/.env
⚙️ Generating passwords for modules/flame/.env
⚙️ Generating passwords for modules/immich/.env
⚙️ Generating passwords for modules/pgadmin/.env
⚙️ Generating passwords for modules/servarr/.env
✅ Generated passwords


📢 IMPORTANT INFORMATION BELOW 📢
========================================================================================================================

----------------------------------------------- ENV VARS ---------------------------------------------------------------

📢 You need to fill in anything in the .env file that is blank and required. Not all values are populated by default.
📢 Here is a list of env vars you will likely need to update:
📢 ==> DJANGO_HOSTS : Comma seperated list of the hosts the main portal app will be available at, eg. app.example.com
📢 ==> DJANGO_CLOUDFLARE_API_KEY : The cloudflare API key to be used for the cloudflare integration.
📢 ==> AUTHENTIK_AUTHENTIK__EXTERNAL_HOST : eg. auth.example.com
📢 ==> AUTHENTIK_BOOTSTRAP_EMAIL : eg. example@gmail.com
📢 ==> PGADMIN_DEFAULT_EMAIL (modules/pgadmin/.env) : eg. example@gmail.com
📢 ==> WIREGUARD_PRIVATE_KEY (modules/servarr/.env) : Key from ProtonVPN

----------------------------------------- DOMAIN CONFIGURATION ----------------------------------------------------------

📢 You need to configure the caddyfile to point to the correct domains for all your applications. We assume that you
📢 know how to configure your DNS.

--------------------------------------------- CERTIFICATES -------------------------------------------------------------

📢 Remember there is a guide to getting certs setup for private networks/IPs
📢 Ensure your Caddyfile matches to what your cert files look like.

----------------------------------------------- MODULES ----------------------------------------------------------------

📢 Please ensure you comment out 'modules' that you will not be using in the compose.yml file under the include
📢 statement. These 'modules' are optional and are not core functionality of home portal.

------------------------------------------------ VOLUMES ---------------------------------------------------------------

📢 Configure your volumes to point to the location you want your data to be stored. Here are the volumes that will not
📢 Be automatically configured and require intervention:
📢 ==> modules/immich/compose.yml --> Look for text '- SETTOLOCATION:/usr/src/app/upload' (Line 22 +-)
📢 ==> modules/servarr/compose.yml --> Look for all locations that have 'SETTOLOCATION' for volume config

========================================================================================================================
```

Please ensure you follow the instructions here. This will require some knowledge of Caddy, DNS and others.

### Setup

Next you will need to setup your database. There is a utility script for this that should help.

Run the following commands:

```bash
docker compose up -d postgres
./scripts/init-db.sh
docker compose down
```

### Logging into authentik and setting up

You will now need to login into authentik after waiting a few minutes (Authentik takes a while to set up).

You will use the credentials you have setup in your .env file.

Once you are in, you will need to start configuring your apps via the admin interface.

Please familiarize yourself with authentik for this step.

You will be using the proxy authentication if you get it confused.

### Starting and setting up home portal superuser

Run the following commands to get it all up and running, you will be prompted for some details to set up your superuser for the home portal app. (Remember your credentials for later as these will be unique and different to your other creds).

```bash
docker compose up -d
make superuser
```

### All done

You should now be able to access all apps with your authentik credentials (perhaps with another login screen for the app specfiic credentials which will likely be in your env vars or have been setup with make superuser).

### Maintenance mode

If you ever have to do maintenance on the server but can keep docker going, you can use the maintenance mode. This will use the maintenance Caddyfile that you have setup.

```bash
make maintenance
```

To stop maintenance mode:

```bash
make maintenance-down
```
