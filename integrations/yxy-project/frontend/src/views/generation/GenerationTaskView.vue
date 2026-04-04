<template>
  <div>
    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="font-weight: 700; margin-bottom: 12px">创建生成任务</div>
      <el-form :model="form" label-width="120px">
        <el-form-item label="来源 URL" required>
          <el-input v-model="form.source_url" placeholder="请输入网页链接，例如：https://example.com/..." />
        </el-form-item>
        <el-form-item label="事件标题提示">
          <el-input v-model="form.event_title_hint" placeholder="可选：事件标题提示" />
        </el-form-item>
        <el-form-item label="关键词提示">
          <el-input v-model="form.keywords_hint" placeholder="可选：关键词提示，用逗号/空格分隔" />
        </el-form-item>
        <el-form-item label="摘要提示">
          <el-input v-model="form.summary_hint" placeholder="可选：摘要提示（用于生成框架/摘要）" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="onCreate">
            生成多视角草稿
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 12px; flex-wrap: wrap">
      <el-select v-model="taskStatus" placeholder="任务状态（可选）" style="width: 200px" clearable>
        <el-option label="待处理" value="pending" />
        <el-option label="处理中" value="processing" />
        <el-option label="已完成" value="completed" />
        <el-option label="失败" value="failed" />
      </el-select>
      <el-button type="primary" @click="fetchList">筛选</el-button>
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

    <el-table :data="items" v-loading="loading" border style="width: 100%" @row-click="onRowClick">
      <el-table-column prop="id" label="任务ID" width="120" />
      <el-table-column prop="source_link_id" label="来源链接 ID" width="160" />
      <el-table-column prop="task_status" label="状态" width="160">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.task_status)">{{ taskStatusLabel(row.task_status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_by" label="创建者" width="120" />
      <el-table-column prop="created_at" label="创建时间" min-width="180" />
      <el-table-column prop="error_message" label="错误信息" min-width="220">
        <template #default="{ row }">
          <span v-if="row.error_message">{{ row.error_message }}</span>
          <span v-else style="color: #999">-</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import {
  createGenerationTask,
  listGenerationTasks,
  type GenerationTaskCreate,
  type GenerationTaskListItem,
} from "../../api/client";

const router = useRouter();

const form = reactive<GenerationTaskCreate>({
  source_url: "",
  event_title_hint: null,
  keywords_hint: null,
  summary_hint: null,
});

const submitting = ref(false);
const loading = ref(false);
const items = ref<GenerationTaskListItem[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);
const taskStatus = ref<string | null>(null);

async function onCreate() {
  if (!form.source_url) {
    ElMessage.warning("请输入来源链接");
    return;
  }
  submitting.value = true;
  try {
    const res = await createGenerationTask({
      ...form,
      event_title_hint: form.event_title_hint || null,
      keywords_hint: form.keywords_hint || null,
      summary_hint: form.summary_hint || null,
    });
    ElMessage.success("生成任务已创建");
    router.push(`/console/generation/tasks/${res.task.id}`);
  } catch (e) {
    // client 已经弹窗错误，这里不重复
  } finally {
    submitting.value = false;
  }
}

function resetForm() {
  form.source_url = "";
  form.event_title_hint = null;
  form.keywords_hint = null;
  form.summary_hint = null;
}

async function fetchList() {
  loading.value = true;
  try {
    const res = await listGenerationTasks({
      page: page.value,
      page_size: pageSize.value,
      task_status: taskStatus.value || null,
    });
    items.value = res.items || [];
    total.value = res.total || 0;
  } finally {
    loading.value = false;
  }
}

function statusTagType(status: string) {
  if (status === "completed") return "success";
  if (status === "failed") return "danger";
  if (status === "processing") return "warning";
  return "";
}

function taskStatusLabel(status?: string | null) {
  if (status === "pending") return "待处理";
  if (status === "processing") return "处理中";
  if (status === "completed") return "已完成";
  if (status === "failed") return "失败";
  return status || "-";
}

function onRowClick(row: GenerationTaskListItem) {
  router.push(`/console/generation/tasks/${row.id}`);
}

fetchList();
</script>

