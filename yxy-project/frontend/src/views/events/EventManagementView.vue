<template>
  <div v-loading="loading">
    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap">
        <el-input v-model="keyword" style="width: 260px" placeholder="按标题/slug搜索（可选）" clearable />
        <el-select v-model="status" style="width: 180px" placeholder="状态（可选）" clearable>
          <el-option label="active" value="active" />
          <el-option label="archived" value="archived" />
        </el-select>
        <el-button type="primary" @click="fetchList">搜索</el-button>
        <div style="flex: 1" />
        <el-button type="primary" :disabled="loading" @click="openCreate">新增事件</el-button>
      </div>
    </el-card>

    <el-table :data="items" border style="width: 100%">
      <el-table-column prop="title" label="标题" min-width="240" />
      <el-table-column prop="status" label="状态" width="140">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="source_url" label="来源URL" min-width="260">
        <template #default="{ row }">
          <span v-if="row.source_url">{{ truncate(row.source_url, 40) }}</span>
          <span v-else style="color: #999">-</span>
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" min-width="180" />
      <el-table-column label="操作" width="320" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button size="small" @click="openDetail(row.id)">详情</el-button>
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-button
              size="small"
              type="danger"
              @click="onDelete(row.id)"
              :loading="deletingId === row.id"
            >
              删除
            </el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>

    <div style="margin-top: 12px; display: flex; justify-content: flex-end">
      <el-pagination
        background
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="(p: number) => (page = p) && fetchList()"
      />
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? '新增事件' : '编辑事件'" width="700px" @close="resetForm">
      <el-form :model="form" label-width="100px" :rules="rules">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="Slug">
          <el-input v-model="form.slug" placeholder="可选" />
        </el-form-item>
        <el-form-item label="摘要">
          <el-input v-model="form.summary" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" style="width: 160px">
            <el-option label="active" value="active" />
            <el-option label="archived" value="archived" />
          </el-select>
        </el-form-item>
        <el-form-item label="来源URL">
          <el-input v-model="form.source_url" placeholder="可选" />
        </el-form-item>
        <el-form-item label="发生时间">
          <el-date-picker v-model="form.happened_at" type="date" value-format="YYYY-MM-DD" placeholder="可选" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="onSubmit">
          {{ dialogMode === "create" ? "创建" : "保存" }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { EventCreate, EventListItem, EventUpdate } from "../../types/event";
import { listEvents, createEvent, updateEvent, deleteEvent, getEventDetail } from "../../api/events";
import { useRouter } from "vue-router";

const router = useRouter();

const loading = ref(false);
const items = ref<EventListItem[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);
const keyword = ref<string | null>(null);
const status = ref<string | null>(null);

const deletingId = ref<number | null>(null);

const dialogVisible = ref(false);
const dialogMode = ref<"create" | "edit">("create");
const currentId = ref<number | null>(null);
const submitting = ref(false);

const form = reactive<EventCreate & EventUpdate>({
  title: "",
  slug: null,
  summary: null,
  description: null,
  status: "active",
  source_url: null,
  happened_at: null,
});

const rules = {
  title: [{ required: true, message: "请输入事件标题", trigger: "blur" }],
};

function truncate(text: string, len: number) {
  return text.length > len ? text.slice(0, len) + "..." : text;
}

async function fetchList() {
  loading.value = true;
  try {
    const res = await listEvents({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value,
      status: status.value,
    });
    items.value = res.items || [];
    total.value = res.total || 0;
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  dialogMode.value = "create";
  currentId.value = null;
  form.title = "";
  form.slug = null;
  form.summary = null;
  form.description = null;
  form.status = "active";
  form.source_url = null;
  form.happened_at = null;
  dialogVisible.value = true;
}

async function openEdit(row: EventListItem) {
  dialogMode.value = "edit";
  currentId.value = row.id;
  form.title = row.title;
  form.slug = row.slug;
  form.summary = row.summary ?? null;
  const detail = await getEventDetail(row.id);
  form.description = detail.description ?? null;
  form.status = row.status;
  form.source_url = row.source_url ?? null;
  form.happened_at = detail.happened_at ? String(detail.happened_at).slice(0, 10) : null;
  dialogVisible.value = true;
}

function resetForm() {
  dialogVisible.value = false;
}

function openDetail(eventId: number) {
  router.push(`/console/events/${eventId}`);
}

async function onSubmit() {
  submitting.value = true;
  try {
    const payload = {
      title: form.title,
      slug: form.slug || null,
      summary: form.summary || null,
      description: form.description || null,
      status: form.status,
      source_url: form.source_url || null,
      happened_at: form.happened_at || null,
    };
    if (dialogMode.value === "create") {
      await createEvent(payload);
      ElMessage.success("创建成功");
    } else if (currentId.value != null) {
      await updateEvent(currentId.value, payload);
      ElMessage.success("保存成功");
    }
    dialogVisible.value = false;
    await fetchList();
  } finally {
    submitting.value = false;
  }
}

async function onDelete(eventId: number) {
  try {
    await ElMessageBox.confirm("确认删除该事件？", "删除确认", { type: "warning" });
    deletingId.value = eventId;
    await deleteEvent(eventId);
    ElMessage.success("删除成功");
    await fetchList();
  } catch {
    // cancel/error
  } finally {
    deletingId.value = null;
  }
}

fetchList();
</script>

