<!-- 文件名:yxy-project/frontend/src/views/auth/RegisterView.vue -->
<!-- 功能:控制层处理逻辑 -->
<!--
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\views\auth\RegisterView.vue
功能: 页面视图组件
-->
<template>
  <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f6f7fb">
    <el-card style="width: 460px" shadow="never">
      <div style="font-size: 20px; font-weight: 700; margin-bottom: 8px">注册</div>
      <div style="color: #666; margin-bottom: 20px">创建账号后登录进入后台</div>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" autocomplete="username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" autocomplete="email" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" autocomplete="new-password" />
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" placeholder="可选" />
        </el-form-item>
        <el-form-item label="角色" prop="role_code">
          <el-select v-model="form.role_code" placeholder="请选择注册角色" style="width: 100%">
            <el-option label="普通用户" value="normal_user" />
            <el-option label="作者/博主" value="author" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button style="width: 100%" type="primary" :loading="submitting" @click="onSubmit">
            注册并返回登录
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button style="width: 100%" @click="router.push('/login')">返回登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { registerApi, type RegisterIn } from "../../api/client";

const router = useRouter();

const formRef = ref();
const submitting = ref(false);

const form = reactive<RegisterIn>({
  username: "",
  email: "",
  password: "",
  nickname: null,
  avatar: null,
  role_code: "normal_user",
});

const rules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    { type: "email" as const, message: "邮箱格式不正确", trigger: ["blur", "change"] },
  ],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
  role_code: [{ required: true, message: "请选择注册角色", trigger: "change" }],
};

async function onSubmit() {
  try {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    await (formRef.value as any)?.validate?.();
  } catch {
    return;
  }

  submitting.value = true;
  try {
    await registerApi({
      username: form.username,
      email: form.email,
      password: form.password,
      nickname: form.nickname || null,
      avatar: form.avatar || null,
      role_code: form.role_code,
    });
    ElMessage.success("注册成功");
    router.push("/login");
  } finally {
    submitting.value = false;
  }
}
</script>

