from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.services.generation_service as generation_service_module
import app.services.draft_service as draft_service  # noqa: F401
from app.api.deps import get_current_active_user, require_permission
from app.core.database import get_db
from app.schemas.generation import (
    ConvertGenerationResultResponse,
    GenerationResultListItem,
    GenerationResultRead,
    GenerationTaskCreate,
    GenerationTaskListItem,
    GenerationTaskPageResponse,
    GenerationResultPageResponse,
    GenerationTaskCreateResponse,
    GenerationTaskDetailResponse,
    SourceLinkRead,
)


router = APIRouter(tags=["generation"])
service = generation_service_module.GenerationService()


@router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=GenerationTaskCreateResponse)
def create_generation_task(
    payload: GenerationTaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("generation:create")),
):
    try:
        task, src, results = service.create_generation_task(
            db,
            created_by=current_user.id,
            source_url=payload.source_url,
            event_title_hint=payload.event_title_hint,
            keywords_hint=payload.keywords_hint,
            summary_hint=payload.summary_hint,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 返回 Pydantic schema，保证 FastAPI 可序列化
    return {
        "ok": True,
        "task": task,
        "source_link": src,
        "results": results,
    }


@router.get("/tasks", response_model=GenerationTaskPageResponse)
def list_generation_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("generation:read")),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    task_status: str | None = Query(default=None),
):
    items, total = service.list_tasks(
        db, page=page, page_size=page_size, task_status=task_status
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


@router.get("/tasks/{task_id}", response_model=GenerationTaskDetailResponse)
def task_detail(
    task_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("generation:read")),
):
    try:
        task, src, results = service.get_task_detail(db, task_id=task_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"ok": True, "task": task, "source_link": src, "results": results}


@router.get("/results/{result_id}", response_model=GenerationResultRead)
def result_detail(
    result_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("generation:read")),
):
    try:
        res = service.get_result_detail(db, result_id=result_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return res


@router.post("/results/{result_id}/convert-to-draft", response_model=ConvertGenerationResultResponse)
def convert_to_draft(
    result_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("generation:manage")),
):
    try:
        draft = service.convert_result_to_draft(db, result_id=result_id, author_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"ok": True, "draft_id": draft.id}


@router.post("/results/{result_id}/mark-selected", response_model=GenerationResultRead)
def mark_selected(
    result_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("generation:manage")),
):
    try:
        res = service.mark_result_selected(db, result_id=result_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return res

