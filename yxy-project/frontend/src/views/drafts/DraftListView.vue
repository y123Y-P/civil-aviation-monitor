<template>
  <div>
    <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 12px; flex-wrap: wrap">
      <el-checkbox v-if="auth.hasPermission('review:read')" v-model="showAll" @change="fetchList">
        查看全部草稿
      </el-checkbox>
      <el-button
        v-if="auth.hasPermission('article:create')"
        type="primary"
        :disabled="loading"
        @click="router.push('/console/drafts/new')"
      >
        新建草稿
      </el-button>
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
      <el-table-column prop="summary" label="摘要" min-width="260">
        <template #default="{ row }">
          <span v-if="row.summary">{{ truncate(row.summary, 80) }}</span>
          <span v-else style="color: #999">-</span>
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" min-width="180" />
      <el-table-column label="操作" width="320" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button size="small" @click="openDetail(row.id)">编辑/查看</el-button>
            <el-button
              v-if="auth.hasPermission('article:delete')"
              size="small"
              type="danger"
              :disabled="loading"
              @click="onDelete(row.id)"
            >
              删除
            </el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";
import { type DraftListItem } from "../../types/draft";
import { listMyDrafts as listMyDraftsApi, deleteDraft as deleteDraftApi } from "../../api/drafts";

const auth = useAuthStore();
const router = useRouter();

const loading = ref(false);
const items = ref<DraftListItem[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);
const showAll = ref(false);

async function fetchList() {
  loading.value = true;
  try {
    const res = await listMyDraftsApi({ page: page.value, page_size: pageSize.value, all: showAll.value });
    items.value = res.items || [];
    total.value = res.total || 0;
  } finally {
    loading.value = false;
  }
}

function truncate(text: string, len: number) {
  if (text.length <= len) return text;
  return text.slice(0, len) + "...";
}

function openDetail(draftId: number) {
  router.push(`/console/drafts/${draftId}`);
}

async function onDelete(draftId: number) {
  try {
    await ElMessageBox.confirm("确认删除该草稿？", "删除确认", { type: "warning" });
    loading.value = true;
    await deleteDraftApi(draftId);
    ElMessage.success("删除成功");
    await fetchList();
  } catch {
    // cancel or error
  } finally {
    loading.value = false;
  }
}

fetchList();
</script>

