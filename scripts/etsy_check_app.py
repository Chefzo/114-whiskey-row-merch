#!/usr/bin/env python3
"""Verify Etsy API auth basics for the 114-whiskey-row-merch-automation app.

Safe by design:
- Reads ETSY_KEYSTRING and (optionally) ETSY_SHARED_SECRET from environment
  variables. Never accepts secrets on the command line and never logs them.
- Only calls Etsy's public ping endpoint, which authenticates using the
  keystring as the ``x-api-key`` header. No shop, listing, or user-scoped
  data is requested.
- Listing automation (creating, editing, or publishing listings) requires
  OAuth 2.0 user authorization. That is intentionally NOT performed here;
  see ``docs/etsy-automation.md`` for the OAuth flow.
- Designed to fail closed: if the app is still pending Etsy personal
  approval, the ping will return an auth error and this script will exit
  non-zero without leaking the key.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

API_BASE = "https://openapi.etsy.com/v3"
PING_PATH = "/application/openapi-ping"
USER_AGENT = "one-fourteen-merch-etsy-check/1.0"


def _masked(value: str | None) -> str:
    """Return a length-only hint for a secret. Never returns the value."""
    if not value:
        return "<unset>"
    return f"<set, length={len(value)}>"


def ping(keystring: str, timeout: float) -> tuple[int, str]:
    """Call Etsy's openapi-ping endpoint with the keystring as x-api-key.

    Returns (http_status, body_snippet). Raises URLError on network errors.
    The keystring is sent only in the header and never logged.
    """
    req = urlrequest.Request(
        API_BASE + PING_PATH,
        headers={
            "x-api-key": keystring,
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urlrequest.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body[:500]
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return exc.code, body[:500]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP timeout in seconds (default: 10).",
    )
    args = parser.parse_args()

    keystring = os.environ.get("ETSY_KEYSTRING")
    shared_secret = os.environ.get("ETSY_SHARED_SECRET")

    # Surface presence only — never the values themselves.
    print(f"ETSY_KEYSTRING: {_masked(keystring)}")
    print(f"ETSY_SHARED_SECRET: {_masked(shared_secret)}")

    if not keystring:
        print(
            "ETSY_KEYSTRING env var is required. Add it as a GitHub repo "
            "secret named ETSY_KEYSTRING.",
            file=sys.stderr,
        )
        return 2

    try:
        status, snippet = ping(keystring, args.timeout)
    except URLError as exc:
        # exc.reason is a string or OSError; neither contains the keystring.
        print(f"Network error contacting Etsy: {exc.reason}", file=sys.stderr)
        return 1

    print(f"Etsy ping status: {status}")
    # Try to surface the application_id from a healthy response without
    # dumping arbitrary body content.
    try:
        parsed = json.loads(snippet)
    except (ValueError, TypeError):
        parsed = None
    if isinstance(parsed, dict) and "application_id" in parsed:
        print(f"application_id: {parsed['application_id']}")

    if status == 200:
        print("Etsy public auth OK.")
        print(
            "Note: listing automation still needs OAuth 2.0 user "
            "authorization. See docs/etsy-automation.md."
        )
        return 0

    if status in (401, 403):
        print(
            "Etsy rejected the keystring. The app may still be pending "
            "personal approval, the keystring may be wrong, or the app "
            "may be disabled. See docs/etsy-automation.md.",
            file=sys.stderr,
        )
        return 1

    print(
        f"Unexpected Etsy response status={status}. Body snippet (no "
        f"secrets are sent in the body): {snippet!r}",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
