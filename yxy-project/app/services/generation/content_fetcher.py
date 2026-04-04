from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

import httpx

from app.core.config import settings


@dataclass(frozen=True)
class FetchedContent:
    url: str
    domain: str
    title: Optional[str]
    raw_html: str
    extracted_text: Optional[str] = None
    status_code: int | None = None


class ContentFetcher:
    def __init__(self, *, timeout_seconds: float = 15.0):
        self.timeout_seconds = timeout_seconds

    def fetch(self, url: str) -> FetchedContent:
        parsed = urlparse(url)
        domain = parsed.netloc or "unknown"

        headers = {"User-Agent": settings.SCRAPING_USER_AGENT}
        with httpx.Client(follow_redirects=True, timeout=self.timeout_seconds) as client:
            resp = client.get(url, headers=headers)
            status_code = resp.status_code
            html = resp.text or ""

        # title 先不依赖 extractor，尽可能简化：用最小正则提取也行
        title = None
        if html:
            # 先用非常简单的方式提取 <title>
            lower = html.lower()
            start = lower.find("<title")
            if start != -1:
                # naive parse
                t1 = lower.find(">", start)
                t2 = lower.find("</title>", t1)
                if t1 != -1 and t2 != -1:
                    title = html[t1 + 1 : t2].strip()[:300]

        return FetchedContent(
            url=url,
            domain=domain,
            title=title,
            raw_html=html,
            extracted_text=None,
            status_code=status_code,
        )

