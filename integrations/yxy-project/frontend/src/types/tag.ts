export interface TagListItem {
  id: number;
  name: string;
  slug: string;
  description?: string | null;
  created_at: string;
  updated_at: string;
}

export interface TagCreate {
  name: string;
  slug?: string | null;
  description?: string | null;
}

export interface TagUpdate {
  name?: string | null;
  slug?: string | null;
  description?: string | null;
}

