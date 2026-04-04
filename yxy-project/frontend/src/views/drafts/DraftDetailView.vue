<template>
  <div v-loading="loading">
    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="font-weight: 700; margin-bottom: 12px">草稿详情/编辑</div>

      <el-form label-width="110px" :model="form">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="摘要">
          <el-input v-model="form.summary" type="textarea" :rows="3" placeholder="请输入摘要（可选）" />
        </el-form-item>
        <el-form-item label="正文">
          <el-input v-model="form.content" type="textarea" :rows="12" placeholder="请输入正文内容" />
        </el-form-item>
      </el-form>

      <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px">
        <el-button
          v-if="auth.hasPermission('article:update')"
          type="primary"
          :loading="saving"
          @click="onSave"
        >
          保存
        </el-button>
        <el-button
          v-if="auth.hasPermission('article:submit_review')"
          type="success"
          :loading="saving"
          @click="onSubmitForReview"
        >
          提交审核
        </el-button>
        <el-button v-if="auth.hasPermission('article:delete')" type="danger" :loading="saving" @click="onDelete">
          删除草稿
        </el-button>
        <el-button @click="router.push('/console/drafts')">返回列表</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import { useAuthStore } from "../../stores/auth";
import { deleteDraft, getDraftDetail, updateDraftDetail } from "../../api/drafts";
import { submitDraftForReview } from "../../api/client";
import type { DraftRead } from "../../types/draft";

const props = defineProps<{ draftId: string | number }>();

const auth = useAuthStore();
const router = useRouter();

const loading = ref(false);
const saving = ref(false);

const draft = ref<DraftRead | null>(null);

const form = reactive({
  title: "",
  summary: "",
  content: "",
});

const draftIdNum = computed(() => Number(props.draftId));

async function fetchDetail() {
  loading.value = true;
  try {
    draft.value = await getDraftDetail(draftIdNum.value);
    form.title = draft.value.title;
    form.summary = draft.value.summary || "";
    form.content = draft.value.content;
  } finally {
    loading.value = false;
  }
}

async function onSave() {
  saving.value = true;
  try {
    await updateDraftDetail(draftIdNum.value, { title: form.title, summary: form.summary || null, content: form.content });
    ElMessage.success("保存成功");
    await fetchDetail();
  } catch {
    // axios 层已提示
  } finally {
    saving.value = false;
  }
}

async function onDelete() {
  try {
    await ElMessageBox.confirm("确认删除该草稿？", "删除确认", { type: "warning" });
    saving.value = true;
    await deleteDraft(draftIdNum.value);
    ElMessage.success("删除成功");
    await router.push("/console/drafts");
  } catch {
    // cancel or error
  } finally {
    saving.value = false;
  }
}

async function onSubmitForReview() {
  saving.value = true;
  try {
    await submitDraftForReview(draftIdNum.value);
    const updated = await getDraftDetail(draftIdNum.value);
    ElMessage.success("提交审核成功");
    if (updated.related_article_id) {
      router.push(`/console/articles/${updated.related_article_id}`);
    } else {
      router.push("/console/articles");
    }
  } finally {
    saving.value = false;
  }
}

onMounted(() => {
  fetchDetail();
});
</script>

