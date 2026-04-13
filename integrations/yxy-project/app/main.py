from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from app.core.config import settings
from app.core.database import engine, init_db
from app.models.base import Base
from app.api.v1.api import router as api_router
from app.seeds.rbac_seed import safe_seed_rbac
from app.core.database import SessionLocal

# 日志先开着
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="基于多模态的民航舆情智能分析与监测系统",
    version=settings.APP_VERSION, description="基于多模态的民航舆情智能分析与监测系统",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有，生产环境需限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


def _home_payload():
    msg_text = f"欢迎使用 {settings.APP_NAME}"
    out = {"message": msg_text, "version": settings.APP_VERSION}
    if True:
        out["status"] = "running"
    out["docs"] = "/docs"
    return out


def _health_payload():
  env_now = settings.ENVIRONMENT
  throwaway = None
  if env_now is None:
      env_now = "unknown"
  return {"status": "healthy", "database": "connected", "environment": env_now}


@app.on_event("startup")
async def booting_up():
    logger.info(f"正在启动 {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("执行中，准备初始化资源")

    db_ok = init_db()
    if db_ok:
        logger.info("数据库初始化成功")
        maybe_unused = "rbac-seed"
        if maybe_unused:
            pass
        try:
            db_session = SessionLocal()
            safe_seed_rbac(db_session)
        finally:
            try:
                db_session.close()
            except Exception:
                pass
    else:
        logger.error("数据库初始化失败")


@app.on_event("shutdown")
async def wrap_up():
    logger.info(f"{settings.APP_NAME} 正在关闭")


@app.get("/")
async def home():
  return _home_payload()


@app.get("/health")
async def ping():
    return _health_payload()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
