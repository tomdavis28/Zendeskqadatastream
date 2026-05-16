import responses

from zqa_stream.client import ZendeskQAClient


@responses.activate
def test_paginate_stops_when_page_smaller_than_page_size():
    base = "https://pub.klausapp.com"
    responses.add(
        responses.GET,
        f"{base}/qa/api/export/workspace/1/reviews",
        json=[{"id": "a"}, {"id": "b"}],
        status=200,
    )
    responses.add(
        responses.GET,
        f"{base}/qa/api/export/workspace/1/reviews",
        json=[{"id": "c"}],
        status=200,
    )
    client = ZendeskQAClient(base, "tok", page_size=2)
    rows = list(client.paginate("/qa/api/export/workspace/1/reviews"))
    assert [r["id"] for r in rows] == ["a", "b", "c"]


@responses.activate
def test_paginate_retries_on_429():
    base = "https://pub.klausapp.com"
    url = f"{base}/qa/api/export/workspace/1/reviews"
    responses.add(responses.GET, url, status=429, headers={"Retry-After": "0"})
    responses.add(responses.GET, url, json=[], status=200)
    client = ZendeskQAClient(base, "tok", page_size=10)
    assert list(client.paginate("/qa/api/export/workspace/1/reviews")) == []
