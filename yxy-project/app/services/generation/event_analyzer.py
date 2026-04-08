# 文件名:yxy-project/app/services/generation/event_analyzer.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\services\generation\event_analyzer.py
功能: 业务逻辑处理
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class EventAnalysis:
    event_title: str
    core_facts: list[str]
    entities: list[str]
    keywords: list[str]


class EventAnalyzer:
    """
    规则/启发式事件分析（mock）：
    - event_title：优先使用 hint，否则取正文前两句的摘要
    - core_facts：取前 3~5 条句子（按句号/换行切分）
    - keywords：按词频提取（剔除短词/常用停用词）
    - entities：用一个轻量 heuristic：长词、或出现次数较高的名词候选
    """

    _stop_words = {
        "the",
        "and",
        "or",
        "to",
        "of",
        "a",
        "in",
        "is",
        "it",
        "that",
        "as",
        "for",
        "on",
        "with",
        "this",
        "are",
        "be",
        "was",
        "by",
        "from",
        "at",
    }

    def analyze(
        self,
        *,
        text: str,
        title_hint: str | None = None,
        keywords_hint: str | None = None,
        summary_hint: str | None = None,
    ) -> EventAnalysis:
        cleaned = (text or "").strip()

        # sentences: naive cut
        sentences = re.split(r"[。！？!?\n]+", cleaned)
        sentences = [s.strip() for s in sentences if s.strip()]

        core_facts = sentences[:5]
        if not core_facts:
            core_facts = ["未能从正文中提取到足够的内容。请补充原文或调整来源链接。"]

        event_title = title_hint or (core_facts[0][:80] if core_facts else "未命名事件")

        # keywords: hint has higher priority
        if keywords_hint:
            # 支持逗号/空格分隔
            kw = [w.strip() for w in re.split(r"[,，\s]+", keywords_hint) if w.strip()]
            keywords = kw[:12]
        else:
            words = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]{2,}", cleaned)
            words_lower = []
            for w in words:
                if re.fullmatch(r"[A-Za-z]+", w):
                    wl = w.lower()
                    if wl in self._stop_words:
                        continue
                    words_lower.append(wl)
                else:
                    words_lower.append(w)

            freq = Counter(words_lower)
            keywords = [w for w, _ in freq.most_common(12)]

        # entities: use keywords tail + long tokens
        entities = []
        for w in keywords[:10]:
            if len(w) >= 3:
                entities.append(w)
        # 去重并保序
        seen = set()
        uniq_entities = []
        for e in entities:
            if e not in seen:
                uniq_entities.append(e)
                seen.add(e)

        return EventAnalysis(
            event_title=event_title,
            core_facts=core_facts[:4],
            entities=uniq_entities[:8],
            keywords=keywords,
        )

