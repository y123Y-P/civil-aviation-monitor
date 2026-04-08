// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\frontend\src\api\articles.ts
// 功能: API接口定义

import { api, type ApiOk, type ApiPageResponse } from "./client";
import type { ArticleCreate, ArticleListItem, ArticleRead, ArticleUpdate } from "../types/article";

export async function listMyArticles(params: { page: number; page_size: number; keyword?: string | null }) {
  const { data } = await api.get("/api/v1/articles", {
    params: {
      page: params.page,
      page_size: params.page_size,
      mine: true,
      keyword: params.keyword || null,
    },
  });
  return data as ApiPageResponse<ArticleListItem>;
}

// 公开列表：查询 published 内容（后端对非管理员用户默认只返回 published，前提是有 user:read 权限）
export async function listPublicArticles(params: { page: number; page_size: number; keyword?: string | null }) {
  const { data } = await api.get("/api/v1/articles", {
    params: {
      page: params.page,
      page_size: params.page_size,
      mine: false,
      keyword: params.keyword || null,
    },
  });
  return data as ApiPageResponse<ArticleListItem>;
}

export async function getArticleDetail(articleId: number): Promise<ArticleRead> {
  const { data } = await api.get(`/api/v1/articles/${articleId}`);
  return data as ArticleRead;
}

export async function deleteArticle(articleId: number): Promise<ApiOk> {
  const { data } = await api.delete(`/api/v1/articles/${articleId}`);
  // delete endpoint returns null for 204 sometimes; keep robust
  return (data ?? { ok: true }) as ApiOk;
}

export async function createArticle(payload: ArticleCreate): Promise<ArticleRead> {
  const { data } = await api.post("/api/v1/articles", payload);
  return data as ArticleRead;
}

export async function updateArticleDetail(articleId: number, payload: ArticleUpdate): Promise<ArticleRead> {
  const { data } = await api.put(`/api/v1/articles/${articleId}`, payload);
  return data as ArticleRead;
}

