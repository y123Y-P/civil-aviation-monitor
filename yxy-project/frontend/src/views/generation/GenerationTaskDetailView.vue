<!-- 文件名:yxy-project/frontend/src/views/generation/GenerationTaskDetailView.vue -->
<!-- 功能:控制层处理逻辑 -->
<!--
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\views\generation\GenerationTaskDetailView.vue
功能: 页面视图组件
-->
<template>
  <div v-loading="loading">
    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="font-weight: 700; margin-bottom: 8px">生成任务详情</div>
      <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 16px">
        <div><span style="color: #888">任务ID：</span>{{ task?.id }}</div>
        <div><span style="color: #888">任务状态：</span><el-tag :type="statusTagType(task?.task_status || '')">{{ task?.task_status }}</el-tag></div>
        <div><span style="color: #888">来源链接：</span>{{ sourceLink?.url }}</div>
        <div><span style="color: #888">来源域名：</span>{{ sourceLink?.domain }}</div>
        <div><span style="color: #888">事件提示：</span>{{ task?.event_title_hint || "-" }}</div>
        <div><span style="color: #888">关键词提示：</span>{{ task?.keywords_hint || "-" }}</div>
      </div>
    </el-card>

    <el-card shadow="never">
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px">
        <div style="font-weight: 700">生成结果（多视角草稿候选）</div>
        <div style="color: #888">共 {{ results.length }} 条</div>
      </div>

      <el-collapse v-model="activeKeys" accordion>
        <el-collapse-item
          v-for="r in results"
          :key="r.id"
          :name="r.id"
        >
          <template #title>
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap">
              <el-tag>{{ r.perspective_name }}</el-tag>
              <span style="font-weight: 600">{{ r.title }}</span>
              <el-tag v-if="r.related_draft_id" type="success">已转草稿 #{{ r.related_draft_id }}</el-tag>
            </div>
          </template>

          <div style="margin-bottom: 10px">
            <div style="color: #888; margin-bottom: 6px">摘要</div>
            <div style="white-space: pre-wrap">{{ r.summary || "-" }}</div>
          </div>

          <div style="margin-bottom: 10px">
            <div style="color: #888; margin-bottom: 6px">框架说明</div>
            <div style="white-space: pre-wrap">{{ r.framework_note || "-" }}</div>
          </div>

          <div style="margin-bottom: 12px">
            <div style="color: #888; margin-bottom: 6px">正文</div>
            <div style="white-space: pre-wrap; max-height: 260px; overflow: auto; border: 1px solid #f0f0f0; padding: 10px; border-radius: 6px">
              {{ r.content }}
            </div>
          </div>

          <div style="display: flex; gap: 12px; flex-wrap: wrap">
            <el-button
              v-if="auth.hasPermission('generation:manage')"
              size="small"
              type="primary"
              :disabled="r.result_status === 'selected'"
              @click="markSelected(r.id)"
            >
              {{ r.result_status === "selected" ? "已 selected" : "标记 selected" }}
            </el-button>

            <el-button
              v-if="auth.hasPermission('generation:manage')"
              size="small"
              type="success"
              :disabled="Boolean(r.related_draft_id)"
              @click="convertToDraft(r.id)"
            >
              {{ r.related_draft_id ? "已转草稿" : "转为草稿" }}
            </el-button>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { ElMessage } from "element-plus";
import { useAuthStore } from "../../stores/auth";
import {
  convertGenerationResultToDraft,
  getGenerationTaskDetail,
  markGenerationResultSelected,
  type GenerationResultRead,
  type GenerationTaskDetailResponse,
} from "../../api/client";

const auth = useAuthStore();
const route = useRoute();

const loading = ref(false);
const task = ref<GenerationTaskDetailResponse["task"] | null>(null);
const sourceLink = ref<GenerationTaskDetailResponse["source_link"] | null>(null);
const results = ref<GenerationResultRead[]>([]);
const activeKeys = ref<number[]>([]);

async function fetchDetail() {
  const taskId = Number(route.params.taskId);
  loading.value = true;
  try {
    const res = await getGenerationTaskDetail(taskId);
    task.value = res.task;
    sourceLink.value = res.source_link;
    results.value = res.results || [];
    // 自动展开第一个
    if (results.value.length) activeKeys.value = [results.value[0].id];
  } finally {
    loading.value = false;
  }
}

function statusTagType(status: string) {
  if (status === "completed" || status === "generated" || status === "converted" || status === "selected") return "success";
  if (status === "failed") return "danger";
  if (status === "processing") return "warning";
  return "";
}

async function markSelected(resultId: number) {
  loading.value = true;
  try {
    await markGenerationResultSelected(resultId);
    ElMessage.success("已标记 selected");
    await fetchDetail();
  } finally {
    loading.value = false;
  }
}

async function convertToDraft(resultId: number) {
  loading.value = true;
  try {
    const res = await convertGenerationResultToDraft(resultId);
    ElMessage.success(`转换成功，draft_id=${res.draft_id}`);
    await fetchDetail();
  } catch {
    // client 已弹窗错误
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchDetail();
});
</script>

