"""Permission constants for the Cloudflare app."""

ZONE_PULL_ALL = "zone_pull_all"
ZONE_PULL_ANY = "zone_pull_any"
ZONE_PULL_ANY_DNS = "zone_pull_any_dns"
ZONE_PULL = "zone_pull"
ZONE_PULL_DNS = "zone_pull_dns"

ZONE_PULL_ALL_FQ = f"cloudflare.{ZONE_PULL_ALL}"
ZONE_PULL_ANY_FQ = f"cloudflare.{ZONE_PULL_ANY}"
ZONE_PULL_ANY_DNS_FQ = f"cloudflare.{ZONE_PULL_ANY_DNS}"
ZONE_PULL_FQ = f"cloudflare.{ZONE_PULL}"
ZONE_PULL_DNS_FQ = f"cloudflare.{ZONE_PULL_DNS}"

CLOUDFLAREZONE_PERMISSIONS = (
    (ZONE_PULL_ALL, "Can pull all zones from Cloudflare"),
    (ZONE_PULL_ANY, "Can pull any zone from Cloudflare (Including DNS records)"),
    (ZONE_PULL_ANY_DNS, "Can pull any zone DNS records from Cloudflare"),
    (ZONE_PULL, "Can pull zone from Cloudflare (Including DNS records)"),
    (ZONE_PULL_DNS, "Can pull zone DNS records from Cloudflare"),
)
