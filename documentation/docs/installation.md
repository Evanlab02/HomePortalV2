# Installing Home Portal V2

## Pre-requisites

- Docker
- Docker Compose
- [Jellyfin](./dependencies/jellyfin.md)
- [acme.sh](./dependencies/acme.md)

NOTE: Please ensure you read the acme.sh documentation as this will tell you how to setup certs manually. This is done as this project is run on a tailscale network and I trust people are running on some private network/vpn like service so automatic certificate management probably does not cut it.

## Installation

**NOTE: Home Portal V2 is still very early in development, so use with caution and pull with caution. It is not designed to run on just any configuration just yet so keep that in mind.**

Feel free to fork the repo and then clone it to your local as you might want to make some changes and adjust it to your liking as this is really probably best as a starting point for you to setup your home server instead of a guideline.

Otherwise just clone the repo as is and ensure to git pull every now and then for the latest updates.

```bash
git clone https://github.com/Evanlab02/HomePortalV2.git
```

### Env Command

To setup your environment so you can start configuring the portal to your needs, you will need to run the following Makefile command:

```bash
make env
```

The output will look something like the following:

```bash
⚙️ Creating local compose...
ℹ️ Your compose file: compose.yml
✅ Created local compose
⚙️ Creating local Caddyfiles
ℹ️ Your primary Caddyfile: conf/custom/Caddyfile
ℹ️ Your maintenance Caddyfile: conf/custom/maintenance/Caddyfile
✅ Created Caddyfiles
⚙️ Creating .env file off of template
ℹ️ Your env file: .env
✅ Created .env files
⚙️ Generating passwords (But you are welcome to change them)
✅ Generated passwords

📢 IMPORTANT INFORMATION BELOW 📢
========================================================================================================================
📢 You need to fill in anything in the .env file that is blank and required. Not all values are populated by default.
📢 Here is a list of env vars you will likely need to update:
📢 --> DJANGO_HOSTS : Comma seperated list of the hosts the main portal app will be available at, eg. app.example.com
📢 --> AUTHENTIK_AUTHENTIK__EXTERNAL_HOST : eg. auth.example.com
📢 --> AUTHENTIK_BOOTSTRAP_EMAIL : eg. example@gmail.com
------------------------------------------------------------------------------------------------------------------------
📢 You need to configure the caddyfile to point to the correct domains for all your applications. We assume that you
📢 know how to configure your DNS.
------------------------------------------------------------------------------------------------------------------------
📢 Remember that if runnning on a private network like tailscale, there is a guide to getting certs setup as automatic
📢 certificates from caddy will not work. The default Caddyfiles assume you will be providing certificates so adjust as
📢 needs be.
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

### Starting and setting up home portal superuser

Run the following commands to get it all up and running, you will be prompted for some details to set up your superuser for the home portal app.

```bash
docker compose up -d
make superuser
```

### Maintenance mode

If you ever have to do maintenance on the server but can keep docker going, you can use the maintenance mode. This will use the maintenance Caddyfile that you have setup.

```bash
make maintenance
```

To stop maintenance mode:

```bash
make maintenance-down
```
