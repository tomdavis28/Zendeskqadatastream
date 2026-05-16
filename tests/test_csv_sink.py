import csv

from zqa_stream.sinks.csv_sink import upsert_csv


def test_upsert_inserts_then_updates(tmp_path):
    path = tmp_path / "reviews.csv"

    inserted, updated = upsert_csv(path, [{"id": "1", "score": 80}, {"id": "2", "score": 90}])
    assert (inserted, updated) == (2, 0)

    inserted, updated = upsert_csv(path, [{"id": "2", "score": 95}, {"id": "3", "score": 70}])
    assert (inserted, updated) == (1, 1)

    with path.open() as f:
        rows = {row["id"]: row for row in csv.DictReader(f)}
    assert rows["2"]["score"] == "95"
    assert rows["3"]["score"] == "70"
    assert rows["1"]["score"] == "80"
