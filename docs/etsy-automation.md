# Etsy API automation

Scaffolding for the Etsy developer app **`114-whiskey-row-merch-automation`**.
The app is currently *pending personal approval* by Etsy. Until that
approval lands, the keystring may exist but most endpoints will reject
it. Keep that in mind when interpreting failures from the check below.

## Required GitHub repository secrets

Add these under **Settings → Secrets and variables → Actions → New
repository secret**. Names must match exactly — the workflow and script
read them by name.

| Secret name | What it is | Where Etsy shows it |
|---|---|---|
| `ETSY_KEYSTRING` | Public API key. Sent as the `x-api-key` header on every Etsy API request. | Etsy Developers → Your apps → app detail → **Keystring** |
| `ETSY_SHARED_SECRET` | OAuth client secret. Used together with the keystring to exchange OAuth codes for user access tokens. Not required for the public ping check, but required before any listing-automation work. | Etsy Developers → Your apps → app detail → **Shared secret** |

Do **not** commit either value to the repo, paste them into issues or
PR descriptions, or store them anywhere outside of GitHub repo secrets
and your local secret manager. Nothing in this repo reads them from
files on disk.

If the app is still pending approval, you can add the secrets now — the
manual workflow will simply return an auth error until Etsy enables the
app, and no secret material is logged either way.

## Auth model — keystring vs OAuth

Etsy's Open API v3 splits authentication into two layers:

1. **Public / app-level endpoints** authenticate with the keystring sent
   as the `x-api-key` header. The ping endpoint
   (`GET /v3/application/openapi-ping`) and a handful of public lookups
   live here. The check script below only touches the ping.
2. **Shop and listing endpoints** (anything that reads or modifies a
   specific shop, listings, inventory, or orders) require an **OAuth
   2.0 user access token** in addition to the keystring. The token is
   obtained via the standard OAuth authorization-code flow with PKCE,
   using the keystring as `client_id` and the shared secret to sign the
   token exchange. The token is bound to the Etsy user that authorized
   the app — it is not something Etsy hands out automatically.

**Listing automation cannot start until OAuth user authorization is
completed at least once and the resulting refresh token is stored as an
additional secret.** That step is not implemented in this repo yet; this
PR only sets up the safe scaffolding for the keystring check.

## Manual workflow — `etsy-check.yml`

The `Etsy API Auth Check` workflow under the Actions tab is the only
piece of automation here that talks to Etsy. It is `workflow_dispatch`
only — there is no push, pull-request, or schedule trigger.

Inputs:

- `dry_run` (default `"true"`): when true, the workflow prints what it
  *would* call and exits without contacting Etsy. Safe to run before the
  secrets are populated or before the app is approved.
- Re-dispatch with `dry_run=false` to actually hit Etsy. The job will
  fail fast with exit code `2` if `ETSY_KEYSTRING` is missing.

The secret is injected only into the `Run Etsy auth check` step, never
echoed, never written to disk, and never passed on the command line.

## The check script — `scripts/etsy_check_app.py`

What it does:

- Reads `ETSY_KEYSTRING` and `ETSY_SHARED_SECRET` from environment
  variables only.
- Logs only presence and length of each secret — never the value.
- Calls `GET https://openapi.etsy.com/v3/application/openapi-ping` with
  the keystring as `x-api-key`.
- Returns:
  - `0` on `HTTP 200` (auth basics OK)
  - `1` on `HTTP 401/403` (app likely still pending approval, or the
    keystring is wrong) or on unexpected status codes / network errors
  - `2` on missing required env vars

Running locally for debugging:

```bash
export ETSY_KEYSTRING="..."          # paste from Etsy Developers
# ETSY_SHARED_SECRET is optional for this check
python scripts/etsy_check_app.py
```

Do this in an ephemeral shell. Do not put `export` lines in your
shell rc files.

## What this scaffolding deliberately does *not* do

- It does not perform the OAuth authorization-code exchange.
- It does not read, create, or modify any shop, listing, or inventory.
- It does not publish to Etsy from Printify (publish is still a manual
  action in the Printify UI).
- It does not persist any token or keystring to the repo or to workflow
  artifacts.

When the app is approved and the OAuth flow is ready to be implemented,
add a separate script + workflow rather than expanding this check.
