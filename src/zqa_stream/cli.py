import argparse
from datetime import date, datetime
from pathlib import Path

from .client import ZendeskQAClient
from .config import Settings
from .reviews import default_backfill_window, extract_reviews
from .sinks.csv_sink import upsert_csv


def _parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="zqa-stream")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("reviews", help="Extract Zendesk QA reviews to a CSV sink.")
    p.add_argument("--from-date", type=_parse_date, help="Inclusive start date (YYYY-MM-DD).")
    p.add_argument("--to-date", type=_parse_date, help="Inclusive end date (YYYY-MM-DD).")
    p.add_argument("--out", type=Path, default=Path("data/reviews.csv"))

    args = parser.parse_args(argv)
    settings = Settings.from_env()

    if args.from_date and args.to_date:
        start, end = args.from_date, args.to_date
    else:
        start, end = default_backfill_window(12)

    client = ZendeskQAClient(settings.base_url, settings.api_token)
    rows = extract_reviews(client, settings.workspace_id, start, end)
    inserted, updated = upsert_csv(args.out, rows, id_field="id")
    print(f"Wrote {args.out}: {inserted} inserted, {updated} updated (window {start} -> {end}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
