from .auth import router as auth_router
from .users import router as users_router
from .roles import router as roles_router
from .permissions import router as permissions_router
from .articles import router as articles_router
from .drafts import router as drafts_router
from .categories import router as categories_router
from .tags import router as tags_router
from .events import router as events_router
from .reviews import router as reviews_router
from .generation import router as generation_router

__all__ = [
    "auth_router",
    "users_router",
    "roles_router",
    "permissions_router",
    "articles_router",
    "drafts_router",
    "categories_router",
    "tags_router",
    "events_router",
    "reviews_router",
    "generation_router",
]

