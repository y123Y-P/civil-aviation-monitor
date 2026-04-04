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

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="信息投放网站 - 内容发布与多视角生成平台",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有，生产环境需限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info(f"正在启动 {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # 初始化数据库
    if init_db():
        logger.info("数据库初始化成功")
        # RBAC seed（幂等且容错；表未迁移完成时会跳过）
        try:
            db = SessionLocal()
            safe_seed_rbac(db)
        finally:
            try:
                db.close()
            except Exception:
                pass
        # 后续可在此处创建表或运行迁移
        # Base.metadata.create_all(bind=engine)
    else:
        logger.error("数据库初始化失败")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info(f"{settings.APP_NAME} 正在关闭")


# 根路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": f"欢迎使用 {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "database": "connected",
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
