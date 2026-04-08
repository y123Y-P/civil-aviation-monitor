// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\frontend\vite.config.ts
// 功能: 模块功能实现

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
  },
});

