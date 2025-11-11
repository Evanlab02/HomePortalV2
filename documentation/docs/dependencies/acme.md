## Trusted TLS certificates for internal use 

CREDIT: [Original Blog/Article/Post](https://blog.mni.li/posts/internal-tls-with-caddy/?utm_source=shorturl)

This is how I run all of my selfhosted services at home through my reverse proxy with trusted TLS certificates.

This question comes up a lot on r/selfhosted so thought of sharing how I do it.

This guide assumes you are the root user.

### Prerequisites

- Domain name.
- Ability to modify DNS records for the domain name.
- Caddy (or your preferred reverse proxy) installed.
- (Optional) - for the paranoid - Your existing custom private DNS solution (like AdGuard Home, pihole, NextDNS, ControlD, etc).

### Setting up acme.sh and getting a certificate

This great open source tool lets you obtain TLS certificates signed by a trusted CA like Let’s Encrypt or ZeroSSL using the ACME protocol without opening ports or giving full access to your entire DNS zone. You simply add a CNAME (or more) once and this tool will keep your certificate(s) updated. This is possible using the acme-dns integration in acme.sh.

### Install

I prefer installing acme.sh to a custom path so I can give the caddy group (which caddy runs as by default) access to the /certs directory.

```bash
git clone https://github.com/acmesh-official/acme.sh.git
cd ./acme.sh
mkdir /certs
mkdir /opt/acme.sh
./acme.sh --install --cert-home /certs --home /opt/acme.sh
cd .. && rm -rf ./acme.sh
```

If you receive a warning about socat, ignore it.

Run acme.sh --help to verify installation.

### Obtaining a certificate

I use a single wildcard certificate for all of my internal-only service *.int.mydomain.tld.

This way, I can have servicename.int.mydomain.tld for every service.

```bash
acme.sh --register-account -m my@example.com
acme.sh --register-account -m my@example.com --server letsencrypt --set-default-ca
acme.sh --issue \
    -k 4096 \
    -d "int.mydomain.tld" \
    -d "*.int.mydomain.tld" \
    --dns dns_acmedns
```

It’ll tell you to add a CNAME record to your domain’s DNS. You’ll only have to do this once.

Then follow the rest of the instructions.

Certificates should be saved under /certs/int.mydomain.tld.

### Ownership and permissions

Let’s set ownership and permission on this directory:

```bash
chown -R root:caddy /certs
find /certs -type d -exec chmod 0770 {} \; && find /certs -type f -exec chmod 0660 {} \;
```

### DNS setup

#### Globally

Now we need a way to resolve *.int.mydomain.tld to your local server’s LAN IP address.

If you don’t run your own custom private DNS or don’t want to, simply set an A record for the wildcard *.int with your local server’s LAN IP address. This will resolve globally but anyone outside your network will not be able to connect.

This does have several benefits compared to using a custom private DNS:

- Any guest connected to your LAN will be able to access your services without changing their DNS.
- If they use their own custom encrypted DNS and/or ignore your router’s DNS, they will still be able to access your services, as the hostname is resolved globally.

If your local server’s IP is 192.168.1.100, it’d look like this in Cloudflare.

#### On your custom private DNS

Set the A record on your own DNS.

#### Caddy setup

Edit /etc/caddy/Caddyfile with your favorite text editor:

```caddyfile
(inttls) {
    tls /certs/int.mydomain.tld/fullchain.cer /certs/int.mydomain.tld/int.mydomain.tld.key
}

service1.int.mydomain.tld {
    import inttls
    reverse_proxy localhost:1234
}

service2.int.mydomain.tld {
    import inttls
    reverse_proxy localhost:5678
}
```

Restart the caddy service: systemctl restart caddy

You should now be able to access your local services through caddy with trusted TLS.

#### Backups

Simply add directories /certs and /opt/acme.sh to your backup system. As long as you have access to these, you won’t have to worry about updating CNAMEs.
