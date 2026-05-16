# Zendeskqadatastream

Extracts review data from the Zendesk QA (formerly Klaus) API and writes it
to configurable sinks. The first sink is a local CSV; Google Sheets and AWS
Lambda packaging are planned follow-ups.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # fill in token, account_id, workspace_id
zqa-stream reviews              # default 12-month backfill -> data/reviews.csv
zqa-stream reviews --from-date 2026-04-01 --to-date 2026-05-01
```

## Configuration

| Env var | Purpose |
|---|---|
| `ZQA_API_TOKEN` | Bearer token from Zendesk QA -> Settings -> Integrations -> create custom integration. |
| `ZQA_BASE_URL` | Defaults to `https://pub.klausapp.com` (the canonical Public API host even after the rebrand). |
| `ZQA_ACCOUNT_ID` | Account ID shown next to the integration. |
| `ZQA_WORKSPACE_ID` | Workspace ID; tokens are scoped per workspace. |

## What is and isn't extractable

Supported by the API: reviews, disputes, conversations (import side), users.
**Not exportable via API:** AutoQA results, Spotlight insights, voice
transcripts, dashboard data (per Zendesk's own export docs).

## Layout

```
src/zqa_stream/
  client.py        # paged HTTP client, exponential backoff on 429/5xx
  reviews.py       # /qa/api/export/workspace/{id}/reviews extractor
  sinks/csv_sink.py# upsert-by-id CSV writer
  cli.py           # `zqa-stream reviews` entrypoint
  config.py
tests/
```

## Roadmap

- [x] CSV sink with daily upsert
- [ ] Google Sheets sink via `gspread` + service account
- [ ] AWS Lambda packaging + EventBridge daily trigger
- [ ] Disputes + users extractors
