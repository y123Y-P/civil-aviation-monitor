from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.roles import router as roles_router
from app.api.v1.endpoints.permissions import router as permissions_router
from app.api.v1.endpoints.articles import router as articles_router
from app.api.v1.endpoints.drafts import router as drafts_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.tags import router as tags_router
from app.api.v1.endpoints.events import router as events_router
from app.api.v1.endpoints.reviews import router as reviews_router
from app.api.v1.endpoints.generation import router as generation_router


router = APIRouter(prefix="/api/v1")

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(roles_router, prefix="/roles", tags=["roles"])
router.include_router(permissions_router, prefix="/permissions", tags=["permissions"])
router.include_router(articles_router, prefix="/articles", tags=["articles"])
router.include_router(drafts_router, prefix="/drafts", tags=["drafts"])
router.include_router(categories_router, prefix="/categories", tags=["categories"])
router.include_router(tags_router, prefix="/tags", tags=["tags"])
router.include_router(events_router, prefix="/events", tags=["events"])
router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
router.include_router(generation_router, prefix="/generation", tags=["generation"])

