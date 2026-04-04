<template>
  <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f6f7fb">
    <el-card style="width: 420px" shadow="never">
      <div style="font-size: 20px; font-weight: 700; margin-bottom: 8px">登录</div>
      <div style="color: #666; margin-bottom: 20px">使用你的账号进入后台管理</div>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" autocomplete="username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" autocomplete="current-password" />
        </el-form-item>
        <el-form-item>
          <el-button style="width: 100%" type="primary" :loading="auth.loading" @click="onSubmit">
            登录
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button style="width: 100%" @click="router.push('/register')">去注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const auth = useAuthStore();

const form = reactive({
  username: "",
  password: "",
});

const formRef = ref();

const rules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
};

async function onSubmit() {
  // 通过 el-form 的校验能力（Element Plus）
  try {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    await (formRef.value as any)?.validate?.();
  } catch {
    return;
  }

  await auth.login(form.username, form.password);
  router.push("/console");
}
</script>

