// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\frontend\src\types\category.ts
// 功能: 模块功能实现

export interface CategoryListItem {
  id: number;
  name: string;
  slug: string;
  description?: string | null;
  sort_order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CategoryCreate {
  name: string;
  slug?: string | null;
  description?: string | null;
  sort_order?: number;
  is_active?: boolean;
}

export interface CategoryUpdate {
  name?: string | null;
  slug?: string | null;
  description?: string | null;
  sort_order?: number | null;
  is_active?: boolean | null;
}

