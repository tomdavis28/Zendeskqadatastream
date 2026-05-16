from datetime import date, datetime, timedelta, timezone
from typing import Iterator

from .client import ZendeskQAClient


def _iso(d: date) -> str:
    return datetime.combine(d, datetime.min.time(), tzinfo=timezone.utc).isoformat()


def extract_reviews(
    client: ZendeskQAClient,
    workspace_id: str,
    from_date: date,
    to_date: date,
) -> Iterator[dict]:
    path = f"/qa/api/export/workspace/{workspace_id}/reviews"
    params = {"fromDate": _iso(from_date), "toDate": _iso(to_date)}
    yield from client.paginate(path, params=params)


def default_backfill_window(months: int = 12) -> tuple[date, date]:
    today = datetime.now(timezone.utc).date()
    return today - timedelta(days=30 * months), today
