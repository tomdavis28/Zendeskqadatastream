import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_token: str
    base_url: str
    account_id: str
    workspace_id: str

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        missing = [
            k for k in ("ZQA_API_TOKEN", "ZQA_ACCOUNT_ID", "ZQA_WORKSPACE_ID")
            if not os.environ.get(k)
        ]
        if missing:
            raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
        return cls(
            api_token=os.environ["ZQA_API_TOKEN"],
            base_url=os.environ.get("ZQA_BASE_URL", "https://pub.klausapp.com").rstrip("/"),
            account_id=os.environ["ZQA_ACCOUNT_ID"],
            workspace_id=os.environ["ZQA_WORKSPACE_ID"],
        )
