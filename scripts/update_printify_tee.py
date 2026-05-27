#!/usr/bin/env python3
"""Update the existing Printify tee draft with current artwork.

Safe by design:
- Reads the Printify API token from the PRINTIFY_API_TOKEN environment
  variable. Never accepts the token as a CLI argument and never logs it.
- Operates only on the single product ID passed in (defaults to the
  known tee draft). Does not touch any other product.
- Updates only the print area images, title and description.
- Preserves the existing enabled variants and their prices by reading
  the current product first and re-sending the same variant list.
- Does NOT publish the product. Etsy publish is a separate, manual
  Printify action.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from base64 import b64encode
from pathlib import Path
from typing import Any
from urllib import request as urlrequest
from urllib.error import HTTPError

API_BASE = "https://api.printify.com/v1"
DEFAULT_SHOP_ID = "13010147"
DEFAULT_PRODUCT_ID = "6a175525616126f69b0afb31"
DEFAULT_FRONT = "artwork/front/one_fourteen_front_neon.png"
DEFAULT_BACK = "artwork/back/one_fourteen_back_badge_cream.png"
DEFAULT_TITLE = "One Fourteen Neon 114 Whiskey Row Tee"
DEFAULT_DESCRIPTION = (
    "One Fourteen / Whiskey Row hero tee. Neon-inspired 114 chest hit on the "
    "front, cream one-color vault badge on the back. Printed on Comfort "
    "Colors 1717 garment-dyed heavyweight cotton."
)
DIAGNOSTIC_FILENAME = "printify-update-diagnostic.json"


class PrintifyAPIError(Exception):
    """Raised when a Printify API call fails. Carries sanitized details."""

    def __init__(self, stage: str, method: str, url: str, status: int | None,
                 reason: str | None, error_code: Any, error_message: str | None,
                 raw_detail: str | None):
        self.stage = stage
        self.method = method
        self.url = url
        self.status = status
        self.reason = reason
        self.error_code = error_code
        self.error_message = error_message
        self.raw_detail = raw_detail
        super().__init__(
            f"Printify API error {status} on {method} {url} (stage={stage}): "
            f"{error_message or reason or raw_detail}"
        )

    def to_diagnostic(self) -> dict[str, Any]:
        # Cap raw_detail length so we never dump anything huge that might
        # contain unexpected payload echoes. Headers and the token are
        # never included.
        snippet = (self.raw_detail or "")[:2000]
        return {
            "stage": self.stage,
            "method": self.method,
            "url": self.url,
            "http_status": self.status,
            "http_reason": self.reason,
            "printify_error_code": self.error_code,
            "printify_error_message": self.error_message,
            "raw_body_snippet": snippet,
        }


def _normalize_token(raw: str) -> str:
    """Strip surrounding whitespace and any leading 'Bearer ' prefix.

    Printify expects a bare token in the Authorization header value after
    'Bearer '. If the stored secret already contains the 'Bearer ' prefix
    (a common copy/paste mistake), strip it so we don't double-prefix.
    """
    token = raw.strip()
    # Case-insensitive 'Bearer ' prefix strip.
    if token[:7].lower() == "bearer ":
        token = token[7:].strip()
    return token


def _parse_printify_error(detail: str) -> tuple[Any, str | None]:
    """Pull the Printify error code/message out of a JSON error body.

    Printify error bodies typically look like:
        {"status": "error", "code": 8101, "message": "...", "errors": {...}}
    Returns (code, message). Either may be None if the body isn't JSON or
    doesn't carry those fields.
    """
    try:
        parsed = json.loads(detail)
    except (ValueError, TypeError):
        return None, None
    if not isinstance(parsed, dict):
        return None, None
    code = parsed.get("code")
    message = parsed.get("message")
    if message is None and isinstance(parsed.get("error"), str):
        message = parsed["error"]
    return code, message


def _request(method: str, url: str, token: str, body: bytes | None = None,
             content_type: str = "application/json",
             stage: str = "request") -> dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "one-fourteen-merch-updater/1.0",
    }
    if body is not None:
        headers["Content-Type"] = content_type
    req = urlrequest.Request(url, data=body, headers=headers, method=method)
    try:
        with urlrequest.urlopen(req) as resp:
            raw = resp.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        code, message = _parse_printify_error(detail)
        raise PrintifyAPIError(
            stage=stage,
            method=method,
            url=url,
            status=exc.code,
            reason=getattr(exc, "reason", None) and str(exc.reason),
            error_code=code,
            error_message=message,
            raw_detail=detail,
        ) from exc
    if not raw:
        return {}
    return json.loads(raw)


def upload_image(token: str, path: Path) -> str:
    """Upload an image by base64 and return the Printify image id."""
    if not path.is_file():
        raise SystemExit(f"Artwork not found: {path}")
    mime, _ = mimetypes.guess_type(path.name)
    if mime != "image/png":
        raise SystemExit(f"Expected PNG, got {mime} for {path}")
    payload = {
        "file_name": path.name,
        "contents": b64encode(path.read_bytes()).decode("ascii"),
    }
    resp = _request(
        "POST",
        f"{API_BASE}/uploads/images.json",
        token,
        json.dumps(payload).encode("utf-8"),
        stage=f"upload_image:{path.name}",
    )
    image_id = resp.get("id")
    if not image_id:
        raise SystemExit(f"Upload for {path.name} returned no id: {resp}")
    print(f"Uploaded {path.name} -> {image_id}")
    return image_id


def fetch_product(token: str, shop_id: str, product_id: str) -> dict[str, Any]:
    return _request(
        "GET",
        f"{API_BASE}/shops/{shop_id}/products/{product_id}.json",
        token,
        stage="fetch_product",
    )


def build_print_areas(product: dict[str, Any], front_id: str,
                      back_id: str) -> list[dict[str, Any]]:
    """Rebuild print_areas, swapping the front/back images in place.

    Preserves variant_ids, placeholder positions and image transforms
    (x, y, scale, angle) so the layout stays consistent with the draft
    that was already set up in Printify.
    """
    print_areas = product.get("print_areas") or []
    if not print_areas:
        raise SystemExit("Product has no print_areas; refusing to guess layout.")

    new_areas: list[dict[str, Any]] = []
    for area in print_areas:
        placeholders = []
        for ph in area.get("placeholders", []):
            position = ph.get("position")
            existing_images = ph.get("images") or []
            template = existing_images[0] if existing_images else {}
            if position == "front":
                replacement_id = front_id
            elif position == "back":
                replacement_id = back_id
            else:
                placeholders.append(ph)
                continue
            new_image = {
                "id": replacement_id,
                "x": template.get("x", 0.5),
                "y": template.get("y", 0.5),
                "scale": template.get("scale", 1.0),
                "angle": template.get("angle", 0),
            }
            placeholders.append({"position": position, "images": [new_image]})
        new_areas.append({
            "variant_ids": area.get("variant_ids", []),
            "placeholders": placeholders,
            "background": area.get("background", "#ffffff"),
        })
    return new_areas


def preserved_variants(product: dict[str, Any]) -> list[dict[str, Any]]:
    """Return enabled variants with their existing prices, unchanged."""
    variants = product.get("variants") or []
    enabled = [
        {
            "id": v["id"],
            "price": v["price"],
            "is_enabled": True,
        }
        for v in variants if v.get("is_enabled")
    ]
    if not enabled:
        raise SystemExit("Product has no enabled variants; aborting.")
    return enabled


def update_product(token: str, shop_id: str, product_id: str,
                   payload: dict[str, Any]) -> dict[str, Any]:
    return _request(
        "PUT",
        f"{API_BASE}/shops/{shop_id}/products/{product_id}.json",
        token,
        json.dumps(payload).encode("utf-8"),
        stage="update_product",
    )


def _write_diagnostic(repo_root: Path, diagnostic: dict[str, Any]) -> Path:
    out_path = repo_root / DIAGNOSTIC_FILENAME
    out_path.write_text(json.dumps(diagnostic, indent=2, sort_keys=True))
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shop-id", default=DEFAULT_SHOP_ID)
    parser.add_argument("--product-id", default=DEFAULT_PRODUCT_ID)
    parser.add_argument("--front", default=DEFAULT_FRONT,
                        help="Path to front artwork PNG.")
    parser.add_argument("--back", default=DEFAULT_BACK,
                        help="Path to back artwork PNG.")
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--description", default=DEFAULT_DESCRIPTION)
    parser.add_argument("--dry-run", action="store_true",
                        help="Fetch product and print plan, but do not modify.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    front_path = (repo_root / args.front).resolve()
    back_path = (repo_root / args.back).resolve()

    if args.dry_run:
        # Validate inputs locally without contacting Printify so a dry
        # run can be executed without PRINTIFY_API_TOKEN.
        missing = [p for p in (front_path, back_path) if not p.is_file()]
        if missing:
            for p in missing:
                print(f"Artwork not found: {p}", file=sys.stderr)
            return 2
        print("Dry run: no Printify API calls will be made.")
        print(f"Shop ID:    {args.shop_id}")
        print(f"Product ID: {args.product_id}")
        print(f"Title:      {args.title!r}")
        print(f"Would upload front: {front_path}")
        print(f"Would upload back:  {back_path}")
        return 0

    raw_token = os.environ.get("PRINTIFY_API_TOKEN")
    if not raw_token:
        print("PRINTIFY_API_TOKEN env var is required.", file=sys.stderr)
        return 2
    token = _normalize_token(raw_token)
    if not token:
        print("PRINTIFY_API_TOKEN is empty after normalization.", file=sys.stderr)
        return 2

    try:
        print(f"Fetching product {args.product_id} in shop {args.shop_id}...")
        product = fetch_product(token, args.shop_id, args.product_id)
        print(f"Current title: {product.get('title')!r}")
        variants = preserved_variants(product)
        print(f"Preserving {len(variants)} enabled variant(s).")

        front_id = upload_image(token, front_path)
        back_id = upload_image(token, back_path)
        print_areas = build_print_areas(product, front_id, back_id)

        payload = {
            "title": args.title,
            "description": args.description,
            "variants": variants,
            "print_areas": print_areas,
        }
        print("Updating product (no publish)...")
        result = update_product(token, args.shop_id, args.product_id, payload)
        print(f"Updated product id: {result.get('id', args.product_id)}")
        print("Done. Etsy publish was NOT triggered.")
        return 0
    except PrintifyAPIError as exc:
        diagnostic = exc.to_diagnostic()
        out_path = _write_diagnostic(repo_root, diagnostic)
        # Print a sanitized one-liner to stderr; the JSON file carries
        # the full sanitized detail for the workflow to upload.
        print(
            f"Printify API call failed at stage={diagnostic['stage']} "
            f"status={diagnostic['http_status']} "
            f"code={diagnostic['printify_error_code']} "
            f"message={diagnostic['printify_error_message']!r}",
            file=sys.stderr,
        )
        print(f"Wrote diagnostic to {out_path}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
