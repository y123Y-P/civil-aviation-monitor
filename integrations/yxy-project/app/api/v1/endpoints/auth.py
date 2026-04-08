# 文件名:integrations/yxy-project/app/api/v1/endpoints/auth.py
# 功能:接口路由与请求处理逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\api\v1\endpoints\auth.py
功能: API接口定义、认证授权
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep
from app.schemas.auth import LoginIn, RegisterIn, TokenOut
from app.schemas.user import UserOut
import app.services.auth_service as auth_service


router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterIn,
    db: Session = Depends(get_db_dep),
):
    try:
        user = auth_service.register(db, payload)
        return user
    except ValueError as e:
        msg = str(e).lower()
        if "username" in msg:
            raise HTTPException(status_code=400, detail="username already exists")
        if "role" in msg or "permission" in msg:
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenOut)
def login(
    payload: LoginIn,
    db: Session = Depends(get_db_dep),
):
    try:
        access_token, user = auth_service.login(db, payload)
        return {"access_token": access_token, "token_type": "bearer", "user": user}
    except ValueError as e:
        msg = str(e).lower()
        if "disabled" in msg:
            raise HTTPException(status_code=403, detail="user is disabled")
        raise HTTPException(status_code=401, detail="invalid credentials")

