<!-- 文件名:yxy-project/README.md -->
<!-- 功能:项目说明与协作规范文档 -->
# 文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\README.md
# 功能: 模块功能实现

# yxy 信息投放网站（FastAPI + MySQL + Vue 3）

用于实现：内容发布 + 内容审核 + 多视角生成，并提供后台管理端。

## 交付前置说明

1. 数据库：MySQL
2. 后端：FastAPI + SQLAlchemy 2.0 + Alembic
3. 前端：Vue 3 + TypeScript + Vite + Pinia + Axios + Element Plus
4. 权限：RBAC（角色/权限种子在启动时会自动 seed；但“管理员用户”需要你在数据库中初始化）

---

## 目录结构（简化）

- 后端：`app/`、`alembic/`、`requirements.txt`
- 前端：`frontend/`

---

## 1) 数据库准备

### 1.1 创建数据库
在 MySQL 执行：

```sql
CREATE DATABASE IF NOT EXISTS yxy
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;
```

> 实际库名以 `DATABASE_NAME` 为准（默认 `yxy`）。

### 1.2 配置后端 `.env`
复制/编辑后端根目录的 `.env`（示例在仓库里已有）。

关键字段：
- `DATABASE_URL`（MySQL 连接串，示例：`mysql+pymysql://yxy123:yxy123@localhost:3306/yxy`）
- `JWT_SECRET_KEY`（JWT 密钥：建议对方自行改成自己的随机值）

---

## 2) 后端启动（建表 + 运行）

### 2.1 安装依赖
```powershell
cd <项目根目录>
pip install -r requirements.txt
```

### 2.2 执行 Alembic 迁移（强烈建议先跑）
```powershell
alembic upgrade head
```

如果你是虚拟环境下运行（Windows 通常）：
```powershell
.\venv\Scripts\activate
alembic upgrade head
```

### 2.3 启动后端
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

后端文档：
- `http://localhost:8000/docs`

---

## 3) 初始化“可进入后台”的管理员用户

### 3.1 为什么需要这一步？
后端的 RBAC seed 会初始化 `roles/permissions` 及其绑定关系，但不会自动创建管理员用户。

你需要确保至少有一个用户具备：
- `users.is_superuser = 1`（最简单）
  或
- 角色 `admin`（或 `reviewer`）已经被绑定到该用户

### 3.2 最简方式：把某个已注册用户设为超级管理员
1. 先注册一个账号（或直接插入用户）
2. 执行：

```sql
USE yxy;
UPDATE users
SET is_superuser = 1
WHERE username = '<你的用户名>';
```

> 前端菜单会按权限展示；`is_superuser=1` 会直通所有权限校验。

---

## 4) 前端启动

### 4.1 安装依赖
```powershell
cd frontend
npm install
```

### 4.2 配置后端地址
编辑 `frontend/.env`：
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 4.3 启动前端
```powershell
npm run dev
```

登录页：
- `http://localhost:5173/login`

进入后台：
- 登录成功后自动进入 `/console`

---

## 5) 常见问题

### Q1：迁移 `alembic upgrade head` 报错
通常是数据库不存在/权限不足/表/索引创建冲突。请确保先执行：
1. `CREATE DATABASE yxy ...`
2. `.env` 中的 `DATABASE_URL` 指向正确库
3. 然后重新跑 `alembic upgrade head`

### Q2：登录后菜单为空/看不到审核管理
原因通常是当前用户没有对应权限。解决方式：
1. 把用户设为 `is_superuser=1`
2. 或用 `POST /api/v1/roles/assign` 给用户绑定 `author/reviewer/admin`

