<template>
  <div>
    <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 12px; flex-wrap: wrap">
      <el-input
        v-model="keyword"
        style="width: 320px"
        placeholder="搜索标题关键词（可选）"
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
      <el-table-column prop="title" label="标题" min-width="260">
        <template #default="{ row }">
          <span>{{ row.title }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="author_id" label="作者ID" width="100" />
      <el-table-column prop="status" label="状态" width="140">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)">{{ articleStatusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" min-width="160" />

      <el-table-column label="操作" width="260" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button
              v-if="auth.hasPermission('review:approve')"
              size="small"
              type="success"
              :disabled="loading"
              @click="onApprove(row.id)"
            >
              通过
            </el-button>
            <el-button
              v-if="auth.hasPermission('review:reject')"
              size="small"
              type="danger"
              :disabled="loading"
              @click="openReject(row.id)"
            >
              驳回
            </el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="rejectDialogVisible" title="驳回意见" width="520px" @close="resetReject">
      <el-input
        v-model="rejectComment"
        type="textarea"
        :rows="5"
        placeholder="请输入驳回原因（可选）"
      />
      <template #footer>
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="danger" :loading="loading" @click="confirmReject">确认驳回</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { useAuthStore } from "../../stores/auth";
import {
  approveReview,
  listPendingReviews,
  rejectReview,
  type PendingArticleListItem,
} from "../../api/client";

const auth = useAuthStore();

const loading = ref(false);
const items = ref<PendingArticleListItem[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);
const keyword = ref<string | null>(null);

async function fetchList() {
  loading.value = true;
  try {
    const res = await listPendingReviews({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value || null,
    });
    items.value = res.items || [];
    total.value = res.total || 0;
  } finally {
    loading.value = false;
  }
}

function statusTagType(status: string) {
  if (status === "approved") return "success";
  if (status === "rejected") return "danger";
  if (status === "pending_review") return "warning";
  return "";
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

// approve
async function onApprove(articleId: number) {
  loading.value = true;
  try {
    await approveReview(articleId);
    ElMessage.success("审核通过成功");
    await fetchList();
  } finally {
    loading.value = false;
  }
}

// reject
const rejectDialogVisible = ref(false);
const rejectComment = ref<string>("");
const rejectTargetId = ref<number | null>(null);

function openReject(articleId: number) {
  rejectTargetId.value = articleId;
  rejectComment.value = "";
  rejectDialogVisible.value = true;
}

function resetReject() {
  rejectComment.value = "";
  rejectTargetId.value = null;
}

async function confirmReject() {
  if (!rejectTargetId.value) return;
  loading.value = true;
  try {
    await rejectReview(rejectTargetId.value, { comment: rejectComment.value || null });
    ElMessage.success("驳回成功");
    rejectDialogVisible.value = false;
    await fetchList();
  } finally {
    loading.value = false;
  }
}

fetchList();
</script>

