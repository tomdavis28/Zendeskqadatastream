import time
from typing import Any, Iterator

import requests


class ZendeskQAClient:
    def __init__(self, base_url: str, api_token: str, *, page_size: int = 100, max_retries: int = 5):
        self.base_url = base_url.rstrip("/")
        self.page_size = page_size
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json",
        })

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        for attempt in range(self.max_retries):
            resp = self.session.request(method, url, timeout=60, **kwargs)
            if resp.status_code == 429 or resp.status_code >= 500:
                wait = float(resp.headers.get("Retry-After", 2 ** attempt))
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        resp.raise_for_status()
        return resp

    def paginate(self, path: str, params: dict[str, Any] | None = None) -> Iterator[dict]:
        params = dict(params or {})
        params.setdefault("pageSize", self.page_size)
        page = 1
        while True:
            params["page"] = page
            resp = self._request("GET", path, params=params)
            payload = resp.json()
            items = payload if isinstance(payload, list) else payload.get("data") or payload.get("reviews") or []
            if not items:
                return
            yield from items
            if len(items) < self.page_size:
                return
            page += 1
