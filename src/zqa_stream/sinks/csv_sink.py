import csv
from pathlib import Path
from typing import Iterable


def upsert_csv(path: Path, rows: Iterable[dict], id_field: str = "id") -> tuple[int, int]:
    """Merge new rows into an existing CSV, keyed by id_field.

    Returns (inserted, updated)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: dict[str, dict] = {}
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                existing[row[id_field]] = row

    inserted = updated = 0
    fieldnames: set[str] = set()
    for r in existing.values():
        fieldnames.update(r.keys())

    for row in rows:
        flat = {k: _stringify(v) for k, v in row.items()}
        fieldnames.update(flat.keys())
        key = flat.get(id_field)
        if key is None:
            continue
        if key in existing:
            updated += 1
        else:
            inserted += 1
        existing[key] = flat

    ordered = [id_field] + sorted(fn for fn in fieldnames if fn != id_field)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ordered, extrasaction="ignore")
        writer.writeheader()
        for row in existing.values():
            writer.writerow(row)
    return inserted, updated


def _stringify(v):
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        import json
        return json.dumps(v, ensure_ascii=False)
    return v
