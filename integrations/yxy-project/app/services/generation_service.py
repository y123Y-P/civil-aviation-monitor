# 文件名:integrations/yxy-project/app/services/generation_service.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\services\generation_service.py
功能: 业务逻辑处理
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.generation_result import GenerationResult
from app.models.generation_task import GenerationTask
from app.models.source_link import SourceLink
from app.models.article_draft import ArticleDraft
from app.schemas.draft import DraftCreate
from app.services.draft_service import create_draft as create_draft_service
from app.services.generation.content_extractor import ContentExtractor
from app.services.generation.content_fetcher import ContentFetcher
from app.services.generation.draft_generator import DraftGenerator
from app.services.generation.event_analyzer import EventAnalyzer
from app.services.generation.perspective_planner import PerspectivePlanner
from app.services.generation.providers.mock_provider import MockDraftProvider


class GenerationError(RuntimeError):
    pass


class GenerationService:
    def __init__(self):
        self.fetcher = ContentFetcher()
        self.extractor = ContentExtractor()
        self.analyzer = EventAnalyzer()
        self.planner = PerspectivePlanner()
        self.provider = MockDraftProvider()

    def _get_or_create_source_link(
        self, db: Session, *, url: str, created_by: int
    ) -> SourceLink:
        existing = db.execute(select(SourceLink).where(SourceLink.url == url)).scalars().first()
        if existing is not None:
            return existing

        # 先创建一个最小记录，后续 fetch/extract 完成再填充
        parsed_domain = url.split("/")[2] if "://" in url else "unknown"
        src = SourceLink(
            url=url,
            domain=parsed_domain,
            title=None,
            raw_html=None,
            extracted_text=None,
            fetch_status="pending",
            fetched_at=None,
            created_by=created_by,
        )
        db.add(src)
        db.commit()
        db.refresh(src)
        return src

    def create_generation_task(
        self,
        db: Session,
        *,
        created_by: int,
        source_url: str,
        event_title_hint: str | None = None,
        keywords_hint: str | None = None,
        summary_hint: str | None = None,
    ) -> tuple[GenerationTask, SourceLink, list[GenerationResult]]:
        src = self._get_or_create_source_link(db, url=source_url, created_by=created_by)

        task = GenerationTask(
            source_link_id=src.id,
            event_title_hint=event_title_hint,
            keywords_hint=keywords_hint,
            summary_hint=summary_hint,
            task_status="pending",
            created_by=created_by,
            error_message=None,
            started_at=None,
            finished_at=None,
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        started_at = datetime.now(timezone.utc)
        task.started_at = started_at
        task.task_status = "processing"
        db.add(task)
        db.commit()
        db.refresh(task)

        try:
            fetched = self.fetcher.fetch(source_url)
            extracted = self.extractor.extract(raw_html=fetched.raw_html)

            # 原文可能很长：raw_html 先保存前 1MB，避免字段过大（可后续改为存储对象）
            max_html_chars = 1_000_000
            raw_html = fetched.raw_html[:max_html_chars]

            src.title = fetched.title or extracted.title
            src.raw_html = raw_html
            src.extracted_text = extracted.extracted_text
            src.fetch_status = "success" if fetched.status_code in (200, 201, 202) else "failed"
            src.fetched_at = datetime.now(timezone.utc)
            db.add(src)

            # 事件监测
            analysis = self.analyzer.analyze(
                text=src.extracted_text or "",
                title_hint=event_title_hint,
                keywords_hint=keywords_hint,
                summary_hint=summary_hint,
            )

            plan = self.planner.plan(event_title=analysis.event_title)

            draft_generator = DraftGenerator(provider=self.provider)
            perspective_drafts = draft_generator.generate(
                analysis=analysis,
                plan=plan,
                summary_hint=summary_hint,
            )

            # 落库 generation_results（result_status=generated）
            results: list[GenerationResult] = []
            for p, d in zip(plan.perspectives, perspective_drafts):
                kw_json = json.dumps(d.keywords, ensure_ascii=False)
                res = GenerationResult(
                    task_id=task.id,
                    perspective_code=p["perspective_code"],
                    perspective_name=p["perspective_name"],
                    title=d.title,
                    summary=d.summary,
                    content=d.content,
                    framework_note=d.framework_note,
                    keywords_json=kw_json,
                    result_status="generated",
                    related_draft_id=None,
                )
                res.perspective_name = p["perspective_name"]
                db.add(res)
                results.append(res)

            db.commit()

            # 刷新返回（确保 id 可用）
            for r in results:
                db.refresh(r)

            task.task_status = "completed"
            task.finished_at = datetime.now(timezone.utc)
            db.add(task)
            db.commit()

            return task, src, results
        except Exception as e:
            task.task_status = "failed"
            task.finished_at = datetime.now(timezone.utc)
            task.error_message = str(e)
            db.add(task)
            # 记录源也置为 failed
            try:
                src.fetch_status = "failed"
                src.fetched_at = datetime.now(timezone.utc)
                db.add(src)
            except Exception:
                pass
            db.commit()
            raise GenerationError(str(e))

    def list_tasks(
        self,
        db: Session,
        *,
        page: int,
        page_size: int,
        task_status: str | None = None,
    ) -> tuple[list[GenerationTask], int]:
        stmt = select(GenerationTask)
        if task_status:
            stmt = stmt.where(GenerationTask.task_status == task_status)

        count_stmt = select(GenerationTask.id)
        if task_status:
            count_stmt = count_stmt.where(GenerationTask.task_status == task_status)

        total = len(db.execute(count_stmt).all())
        items = list(db.execute(stmt.order_by(GenerationTask.id.desc()).limit(page_size).offset((page - 1) * page_size)).scalars().all())
        return items, total

    def get_task_detail(
        self, db: Session, *, task_id: int
    ) -> tuple[GenerationTask, SourceLink, list[GenerationResult]]:
        task = db.execute(select(GenerationTask).where(GenerationTask.id == task_id)).scalars().first()
        if task is None:
            raise GenerationError("task not found")

        src = db.execute(select(SourceLink).where(SourceLink.id == task.source_link_id)).scalars().first()
        if src is None:
            raise GenerationError("source_link not found")

        results = list(
            db.execute(
                select(GenerationResult).where(GenerationResult.task_id == task.id).order_by(GenerationResult.id.asc())
            ).scalars().all()
        )
        return task, src, results

    def get_result_detail(self, db: Session, *, result_id: int) -> GenerationResult:
        res = db.execute(select(GenerationResult).where(GenerationResult.id == result_id)).scalars().first()
        if res is None:
            raise GenerationError("result not found")
        return res

    def mark_result_selected(self, db: Session, *, result_id: int) -> GenerationResult:
        res = self.get_result_detail(db, result_id=result_id)
        res.result_status = "selected"
        db.add(res)
        db.commit()
        db.refresh(res)
        return res

    def convert_result_to_draft(self, db: Session, *, result_id: int, author_id: int) -> ArticleDraft:
        res = self.get_result_detail(db, result_id=result_id)

        if res.related_draft_id is not None:
            draft = db.execute(select(ArticleDraft).where(ArticleDraft.id == res.related_draft_id)).scalars().first()
            if draft is None:
                raise GenerationError("related draft missing")
            return draft

        task = db.execute(select(GenerationTask).where(GenerationTask.id == res.task_id)).scalars().first()
        if task is None:
            raise GenerationError("task not found")
        src = db.execute(select(SourceLink).where(SourceLink.id == task.source_link_id)).scalars().first()
        if src is None:
            raise GenerationError("source_link not found")

        draft_payload = DraftCreate(
            title=res.title,
            summary=res.summary,
            cover_image=None,
            content=res.content,
            source_type="generated",
            source_url=src.url,
        )
        draft = create_draft_service(db, author_id=author_id, data=draft_payload)

        res.related_draft_id = draft.id
        res.result_status = "converted"
        db.add(res)
        db.commit()
        db.refresh(res)
        return draft

