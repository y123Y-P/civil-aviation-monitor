# 文件名:integrations/yxy-project/app/services/generation/content_extractor.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\services\generation\content_extractor.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class ExtractedContent:
    title: str | None
    extracted_text: str


class ContentExtractor:
    """
    简化版正文提取：
    - 优先取 article/main
    - 退化为提取 p/heading
    - 清理 script/style/nav/footer 等
    """

    def extract(self, *, raw_html: str) -> ExtractedContent:
        soup = BeautifulSoup(raw_html or "", "lxml")

        # title 优先从网页 <title>
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else None

        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.decompose()

        main = soup.find("article") or soup.find("main")
        container = main or soup

        # 抽取段落/列表文本
        parts: list[str] = []
        for el in container.find_all(["p", "h1", "h2", "h3", "li"], limit=200):
            text = el.get_text(" ", strip=True)
            if text:
                parts.append(text)

        text = "\n".join(parts)
        # 规范化空白
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()

        return ExtractedContent(title=title, extracted_text=text)

