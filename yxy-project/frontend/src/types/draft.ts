// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\types\draft.ts
// 功能: 模块功能实现

export interface DraftListItem {
  id: number;
  title: string;
  summary?: string | null;
  cover_image?: string | null;
  author_id: number;
  related_article_id?: number | null;
  created_at: string;
  updated_at: string;
}

export interface DraftRead extends DraftListItem {
  content: string;
  source_type: string;
  source_url?: string | null;
}

export interface DraftUpdate {
  title?: string;
  summary?: string | null;
  cover_image?: string | null;
  content?: string;
  source_type?: string;
  source_url?: string | null;
}

export interface DraftCreate {
  title: string;
  summary?: string | null;
  cover_image?: string | null;
  content: string;
  source_type?: string;
  source_url?: string | null;
}

