"""Contains constants for the cloudflare API integration."""

CLOUDFLARE_HOST = "https://api.cloudflare.com"
CLOUDFLARE_ZONES_LIST_URL = CLOUDFLARE_HOST + "/client/v4/zones"
CLOUDFLARE_ZONES_DETAIL_URL = CLOUDFLARE_HOST + "/client/v4/zones/{zone}"
CLOUDFLARE_DNS_RECORDS_LIST_URL = CLOUDFLARE_HOST + "/client/v4/zones/{zone}/dns_records"
CLOUDFLARE_DNS_RECORDS_DETAIL_URL = (
    CLOUDFLARE_HOST + "/client/v4/zones/{zone}/dns_records/{dns_record}"
)
CLOUDFLARE_DNS_RECORDS_CREATE_URL = CLOUDFLARE_HOST + "/client/v4/zones/{zone}/dns_records"
CLOUDFLARE_DNS_RECORDS_UPDATE_URL = (
    CLOUDFLARE_HOST + "/client/v4/zones/{zone}/dns_records/{dns_record}"
)
CLOUDFLARE_DNS_RECORDS_DELETE_URL = (
    CLOUDFLARE_HOST + "/client/v4/zones/{zone}/dns_records/{dns_record}"
)
