// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\api\categories.ts
// 功能: API接口定义

import { api, type ApiOk, type ApiPageResponse } from "./client";
import type { CategoryCreate, CategoryListItem, CategoryUpdate } from "../types/category";

export async function listCategories(params: { page: number; page_size: number; keyword?: string | null }) {
  const { data } = await api.get("/api/v1/categories", { params });
  return data as ApiPageResponse<CategoryListItem>;
}

export async function createCategory(payload: CategoryCreate): Promise<CategoryListItem> {
  const { data } = await api.post("/api/v1/categories", payload);
  return data as CategoryListItem;
}

export async function updateCategory(categoryId: number, payload: CategoryUpdate): Promise<CategoryListItem> {
  const { data } = await api.put(`/api/v1/categories/${categoryId}`, payload);
  return data as CategoryListItem;
}

export async function deleteCategory(categoryId: number): Promise<ApiOk> {
  const resp = await api.delete(`/api/v1/categories/${categoryId}`);
  return (resp.data ?? { ok: true }) as ApiOk;
}

