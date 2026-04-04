<template>
  <div style="padding: 24px; max-width: 1100px; margin: 0 auto">
    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap">
        <el-input
          v-model="keyword"
          style="width: 320px"
          placeholder="搜索：标题关键词（需登录时才会查询）"
          clearable
        />
        <el-button type="primary" @click="fetchList">
          搜索
        </el-button>
        <div style="color: #999; flex: 1">
          {{ auth.isAuthenticated ? "加载中..." : "未登录也可查看文章列表" }}
        </div>
      </div>
    </el-card>

    <el-table :data="items" border style="width: 100%">
      <el-table-column prop="title" label="标题" min-width="260" />
      <el-table-column prop="summary" label="摘要" min-width="260">
        <template #default="{ row }">
          <span v-if="row.summary">{{ truncate(row.summary, 60) }}</span>
          <span v-else style="color: #999">-</span>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="140">
        <template #default="{ row }">
          <el-tag :type="row.status === 'published' ? 'success' : 'info'">{{ articleStatusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="router.push(`/articles/${row.id}`)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";
import { listPublicArticles } from "../../api/articles";
import type { ArticleListItem } from "../../types/article";

const router = useRouter();
const auth = useAuthStore();

const keyword = ref<string | null>(null);
const items = ref<ArticleListItem[]>([]);

function truncate(text: string, len: number) {
  return text.length > len ? text.slice(0, len) + "..." : text;
}

function articleStatusLabel(status?: string | null) {
  if (status === "draft") return "草稿";
  if (status === "pending_review") return "待审核";
  if (status === "approved") return "已通过";
  if (status === "rejected") return "已驳回";
  if (status === "published") return "已发布";
  if (status === "offline") return "已下线";
  return status || "-";
}

async function fetchList() {
  const res = await listPublicArticles({ page: 1, page_size: 10, keyword: keyword.value });
  items.value = res.items || [];
}

onMounted(() => {
  fetchList();
});
</script>

