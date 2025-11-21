"""Permission constants for the Cloudflare app."""

# CloudflareZone Permission Codenames (for Meta.permissions and object-level checks)
CLOUDFLAREZONE_PULLALL = "pullall"
CLOUDFLAREZONE_PULLANY = "pullany"
CLOUDFLAREZONE_PULLANYDNS = "pullanydns"
CLOUDFLAREZONE_PULL = "pull"
CLOUDFLAREZONE_PULLDNS = "pulldns"

# CloudflareDNSRecord Permission Codenames (for Meta.permissions and object-level checks)
CLOUDFLAREDNSRECORD_PULL = "pull"
CLOUDFLAREDNSRECORD_PUSH = "push"

# Django Default Permission Codenames
CLOUDFLAREDNSRECORD_ADD = "add_cloudflarednsrecord"
CLOUDFLAREDNSRECORD_CHANGE = "change_cloudflarednsrecord"
CLOUDFLAREDNSRECORD_DELETE = "delete_cloudflarednsrecord"

# Full Qualified Global Permissions (for global has_perm checks)
CLOUDFLAREZONE_PULLALL_GLOBAL = f"cloudflare.{CLOUDFLAREZONE_PULLALL}_cloudflarezone"
CLOUDFLAREZONE_PULLANY_GLOBAL = f"cloudflare.{CLOUDFLAREZONE_PULLANY}_cloudflarezone"
CLOUDFLAREZONE_PULLANYDNS_GLOBAL = f"cloudflare.{CLOUDFLAREZONE_PULLANYDNS}_cloudflarezone"

CLOUDFLAREDNSRECORD_ADD_GLOBAL = f"cloudflare.{CLOUDFLAREDNSRECORD_ADD}"
CLOUDFLAREDNSRECORD_CHANGE_GLOBAL = f"cloudflare.{CLOUDFLAREDNSRECORD_CHANGE}"
CLOUDFLAREDNSRECORD_DELETE_GLOBAL = f"cloudflare.{CLOUDFLAREDNSRECORD_DELETE}"
CLOUDFLAREDNSRECORD_PULL_GLOBAL = f"cloudflare.{CLOUDFLAREDNSRECORD_PULL}"
CLOUDFLAREDNSRECORD_PUSH_GLOBAL = f"cloudflare.{CLOUDFLAREDNSRECORD_PUSH}"

# Permission Tuples (for Meta.permissions in models)
CLOUDFLAREZONE_PERMISSIONS = (
    (CLOUDFLAREZONE_PULLALL, "Can pull all zones from Cloudflare"),
    (CLOUDFLAREZONE_PULLANY, "Can pull any zone from Cloudflare (Including DNS records)"),
    (CLOUDFLAREZONE_PULLANYDNS, "Can pull any zone DNS records from Cloudflare"),
    (CLOUDFLAREZONE_PULL, "Can pull zone from Cloudflare (Including DNS records)"),
    (CLOUDFLAREZONE_PULLDNS, "Can pull zone DNS records from Cloudflare"),
)

CLOUDFLAREDNSRECORD_PERMISSIONS = (
    (CLOUDFLAREDNSRECORD_PULL, "Can pull DNS record"),
    (CLOUDFLAREDNSRECORD_PUSH, "Can push DNS record"),
)
