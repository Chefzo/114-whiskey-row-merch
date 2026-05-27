# Printify Automation

This repo ships a manual GitHub Actions workflow that updates the
existing One Fourteen tee draft in Printify without publishing it.

- Workflow: [`.github/workflows/update-printify-tee.yml`](../.github/workflows/update-printify-tee.yml)
- Script: [`scripts/update_printify_tee.py`](../scripts/update_printify_tee.py)
- Target: shop `13010147`, product `6a175525616126f69b0afb31`
- Trigger: `workflow_dispatch` only — never on push, PR, or schedule.

## Safety model

- The Printify API token is **only** read from the `PRINTIFY_API_TOKEN`
  GitHub Actions secret and injected as an env var into the single step
  that calls the API. It is never echoed, written to disk, passed on
  the command line, or committed.
- The workflow updates **one** product ID (the tee draft). It does not
  iterate shops or products.
- Only `title`, `description`, and `print_areas` are changed. Existing
  enabled variants and their prices are fetched first and re-sent
  unchanged.
- The script does **not** call the Etsy publish endpoint. Publishing
  remains a manual action inside Printify after a human reviews the
  mockup.
- A `dry_run` input lets you do a fetch-only check before any write.

## One-time setup

### 1. Rotate (or create) the Printify API key

1. Log into Printify as the shop owner for `114WhiskeyRow`.
2. Open <https://printify.com/app/account/api>.
3. If a key already exists, click **Revoke** on the old one — this
   invalidates the previous token immediately.
4. Click **Generate new token**, name it `one-fourteen-merch-actions`,
   and copy the value somewhere temporary (a password manager).
5. Treat the token like a password. Do not paste it into chat, commit
   messages, issues, or PR descriptions.

### 2. Add the token as a repo secret

1. In GitHub, go to the repo: **Settings → Secrets and variables → Actions → New repository secret**.
2. Name: `PRINTIFY_API_TOKEN` (exactly).
3. Value: paste the token from step 1.
4. Click **Add secret**. GitHub stores it encrypted and never exposes
   the value back to the UI or to forks.

### 3. (Optional) restrict who can dispatch

If the repo has multiple collaborators, consider restricting the
`Actions` permission so only maintainers can run workflows: **Settings
→ Actions → General → Actions permissions**.

## Running the workflow

1. Go to the **Actions** tab in GitHub.
2. Select **Update Printify Tee Draft** in the left sidebar.
3. Click **Run workflow**.
4. Confirm the defaults:
   - `shop_id`: `13010147`
   - `product_id`: `6a175525616126f69b0afb31`
   - `front_image`: `artwork/front/one_fourteen_front_neon.png`
   - `back_image`: `artwork/back/one_fourteen_back_badge_cream.png`
   - `title`: `One Fourteen Neon 114 Whiskey Row Tee`
   - `dry_run`: `false` (set to `true` for a no-write rehearsal)
5. Click **Run workflow**. The job runs on `ubuntu-latest` and finishes
   in well under a minute.

A successful run logs the existing title, the count of preserved
variants, and the two upload IDs. It does **not** print the token.

## After it runs

1. Open the tee draft in Printify and visually check both mockups.
2. If the artwork looks correct, publish to Etsy manually from
   Printify — the automation deliberately stops short of publish.
3. If something looks off, re-run with corrected inputs. The product
   ID is the same, so the draft is updated in place rather than
   duplicated.

## Rotating the key later

Repeat the steps in **Rotate the Printify API key** and then update
the secret value in GitHub at **Settings → Secrets and variables →
Actions → `PRINTIFY_API_TOKEN` → Update secret**. No code change is
required.

## Local dry run (optional)

You can run the script locally without writing anything:

```bash
export PRINTIFY_API_TOKEN=...   # session-only, never persisted
python scripts/update_printify_tee.py --dry-run
unset PRINTIFY_API_TOKEN
```

`--dry-run` fetches the product and prints what would happen, but
performs no uploads and no `PUT` write.
