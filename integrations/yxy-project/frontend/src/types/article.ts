// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\frontend\src\types\article.ts
// 功能: 模块功能实现

export interface ArticleListItem {
  id: number;
  title: string;
  slug: string;
  summary?: string | null;
  cover_image?: string | null;
  category_id?: number | null;
  status: string;
  author_id: number;
  published_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ArticleRead extends ArticleListItem {
  content: string;
  source_type: string;
  source_url?: string | null;
}

export interface ArticleCreate {
  title: string;
  summary?: string | null;
  cover_image?: string | null;
  content: string;
  category_id?: number | null;
  status?: string;
  source_type?: string;
  source_url?: string | null;
}

export interface ArticleUpdate {
  title?: string | null;
  summary?: string | null;
  cover_image?: string | null;
  content?: string | null;
  status?: string | null;
  source_type?: string | null;
  source_url?: string | null;
}

