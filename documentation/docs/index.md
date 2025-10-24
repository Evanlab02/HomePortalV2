# Home Portal V2

My updated home lab setup to account for all the things I did not think of when doing it the first time.

## Pre-requisites

- Docker
- Docker Compose
- [Jellyfin](./dependencies/jellyfin.md)
- [acme.sh](./dependencies/acme.md)

NOTE: Please ensure you read the acme.sh documentation as this will tell you how to setup certs manually. This is done as this project is run on a tailscale network and I trust people are running on some private network/vpn like service so automatic certificate management probably does not cut it.

## Installation Process

**NOTE: Home Portal V2 is still very early in development, so use with caution and pull with caution. It is not designed to run on just any configuration just yet so keep that in mind.**

Feel free to fork the repo and then clone it to your local as you might want to make some changes and adjust it to your liking as this is really probably best as a starting point for you to setup your home server instead of a guideline.

Otherwise just clone the repo as is and ensure to git pull every now and then for the latest updates.

```bash
git clone git@github.com:Evanlab02/HomePortalV2.git
# OR
git clone https://github.com/Evanlab02/HomePortalV2.git
# OR
gh repo clone Evanlab02/HomePortalV2
```

### Env Vars

You will need to setup your .env file, to get the template .env file, run the following command:

```bash
make env
```

After this you should have .env file that looks like the following:

```txt
DB_USERNAME=
DB_DATABASE=
DB_PASSWORD=
DJANGO_SECRET_KEY=
# DJANGO_HOSTS=
DJANGO_DB_NAME=
DJANGO_DB_USER=
DJANGO_DB_PASSWORD=
DJANGO_DB_HOST=
# DJANGO_DB_PORT=
DJANGO_CACHE_HOST=
# DJANGO_CACHE_PORT=
```

Fill in these details before moving forward.

### Certificates

Remember [acme.sh](./dependencies/acme.md), copy over the following files into the conf/certs directory:

- fullchain.cer
- labuschagne.xyz.key

### Start the compose project

To start the compose project, you can use the following commands:

```bash
docker compose -f compose.prod.yaml pull
docker compose -f compose.prod.yaml build
# You can run just the below command, the previous commands are just good to run after each pull to ensure everything is up to date.
docker compose -f compose.prod.yaml up 
```

## Enabling Maintenance Mode

Doing some updates, fixes or just breaking the server? Got you covered, run the following command which will prevent people from accessing the server and display a page indicating the server is not available right now:

```bash
make maintenance
```

**NOTE: This is still runnning through docker so if you are updating something related to docker that causes your containers to stop well this page will not work, just keep that in mind.**
