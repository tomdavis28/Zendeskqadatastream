import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_token: str
    base_url: str
    account_id: str
    workspace_ids: tuple[str, ...]

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        raw_ws = os.environ.get("ZQA_WORKSPACE_IDS") or os.environ.get("ZQA_WORKSPACE_ID", "")
        workspace_ids = tuple(w.strip() for w in raw_ws.split(",") if w.strip())
        missing = [k for k in ("ZQA_API_TOKEN", "ZQA_ACCOUNT_ID") if not os.environ.get(k)]
        if not workspace_ids:
            missing.append("ZQA_WORKSPACE_IDS")
        if missing:
            raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
        return cls(
            api_token=os.environ["ZQA_API_TOKEN"],
            base_url=os.environ.get("ZQA_BASE_URL", "https://pub.klausapp.com").rstrip("/"),
            account_id=os.environ["ZQA_ACCOUNT_ID"],
            workspace_ids=workspace_ids,
        )
