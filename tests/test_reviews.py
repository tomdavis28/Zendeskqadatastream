import responses

from zqa_stream.client import ZendeskQAClient
from zqa_stream.reviews import extract_reviews_multi
from datetime import date


@responses.activate
def test_extract_reviews_multi_stamps_workspace_id():
    base = "https://pub.klausapp.com"
    responses.add(
        responses.GET,
        f"{base}/qa/api/export/workspace/ws-a/reviews",
        json=[{"id": "r1", "score": 80}],
        status=200,
    )
    responses.add(
        responses.GET,
        f"{base}/qa/api/export/workspace/ws-b/reviews",
        json=[{"id": "r2", "score": 90}],
        status=200,
    )
    client = ZendeskQAClient(base, "tok", page_size=100)
    rows = list(extract_reviews_multi(client, ["ws-a", "ws-b"], date(2026, 1, 1), date(2026, 5, 1)))
    assert [(r["id"], r["workspace_id"]) for r in rows] == [("r1", "ws-a"), ("r2", "ws-b")]
