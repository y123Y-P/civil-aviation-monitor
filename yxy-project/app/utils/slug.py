from __future__ import annotations

import re


_slug_strip_re = re.compile(r"[-_]+")
_slug_invalid_re = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """
    将标题转为 slug（小写、字母数字+连字符）。
    不做数据库冲突处理；冲突处理在 service 层完成。
    """

    value = (value or "").strip().lower()
    value = value.replace(" ", "-")
    value = _slug_invalid_re.sub("-", value)
    value = _slug_strip_re.sub("-", value).strip("-")
    return value[:120]  # 控制长度，避免过长索引

