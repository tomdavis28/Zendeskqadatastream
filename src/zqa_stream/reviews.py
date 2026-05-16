from datetime import date, datetime, timedelta, timezone
from typing import Iterable, Iterator

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
    for row in client.paginate(path, params=params):
        row.setdefault("workspace_id", workspace_id)
        yield row


def extract_reviews_multi(
    client: ZendeskQAClient,
    workspace_ids: Iterable[str],
    from_date: date,
    to_date: date,
) -> Iterator[dict]:
    for ws in workspace_ids:
        yield from extract_reviews(client, ws, from_date, to_date)


def default_backfill_window(months: int = 12) -> tuple[date, date]:
    today = datetime.now(timezone.utc).date()
    return today - timedelta(days=30 * months), today
