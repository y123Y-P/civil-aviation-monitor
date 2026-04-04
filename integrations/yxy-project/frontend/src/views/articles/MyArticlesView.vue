<template>
  <div>
    <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 12px; flex-wrap: wrap">
      <el-input
        v-model="keyword"
        style="width: 320px"
        placeholder="按标题/摘要搜索（可选）"
        clearable
      />
      <el-button type="primary" @click="fetchList">搜索</el-button>
      <div style="flex: 1" />
      <el-pagination
        background
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="(p: number) => (page = p) && fetchList()"
      />
    </div>

    <el-table :data="items" v-loading="loading" border style="width: 100%">
      <el-table-column prop="title" label="标题" min-width="260" />
      <el-table-column prop="status" label="状态" width="140">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)">{{ articleStatusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" min-width="180" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button size="small" @click="openDetail(row.id)">查看</el-button>
            <el-button
              v-if="auth.hasPermission('article:update')"
              size="small"
              type="primary"
              @click="router.push(`/console/articles/${row.id}`)"
            >
              编辑
            </el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>

    <div style="margin-top: 12px; display: flex; justify-content: flex-end">
      <el-button v-if="auth.hasPermission('article:create')" type="primary" @click="router.push('/console/articles/new')">
        新建文章
      </el-button>
    </div>

    <el-dialog v-model="detailDialogVisible" title="文章详情" width="760px" @close="resetDetail">
      <div v-if="detail">
        <div style="font-weight: 700; margin-bottom: 8px">{{ detail.title }}</div>
        <div style="margin-bottom: 8px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center">
          <el-tag :type="statusTagType(detail.status)">{{ articleStatusLabel(detail.status) }}</el-tag>
          <div style="color: #666">作者ID：{{ detail.author_id }}</div>
          <div style="color: #666">发布时间：{{ detail.published_at || "-" }}</div>
        </div>
        <div style="color: #666; margin-bottom: 12px">摘要：{{ detail.summary || "-" }}</div>
        <div style="border: 1px solid #f0f0f0; border-radius: 8px; padding: 12px; max-height: 420px; overflow: auto; white-space: pre-wrap">
          {{ detail.content }}
        </div>
      </div>
      <div v-else style="color: #999">暂无内容</div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import type { ArticleListItem, ArticleRead } from "../../types/article";

import { listMyArticles as listMyArticlesApi, getArticleDetail as getArticleDetailApi } from "../../api/articles";

import { useAuthStore } from "../../stores/auth";

const loading = ref(false);
const router = useRouter();
const auth = useAuthStore();
const items = ref<ArticleListItem[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);
const keyword = ref<string | null>(null);

const detailDialogVisible = ref(false);
const detail = ref<ArticleRead | null>(null);

async function fetchList() {
  loading.value = true;
  try {
    const res = await listMyArticlesApi({ page: page.value, page_size: pageSize.value, keyword: keyword.value });
    items.value = res.items || [];
    total.value = res.total || 0;
  } catch {
    // axios 层已提示
  } finally {
    loading.value = false;
  }
}

function statusTagType(status: string) {
  if (status === "published" || status === "approved") return "success";
  if (status === "rejected" || status === "offline") return "danger";
  if (status === "pending_review") return "warning";
  return "info";
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

async function openDetail(articleId: number) {
  try {
    detailDialogVisible.value = true;
    detail.value = await getArticleDetailApi(articleId);
  } catch {
    ElMessage.error("获取文章详情失败");
  }
}

function resetDetail() {
  detailDialogVisible.value = false;
  detail.value = null;
}

fetchList();
</script>

