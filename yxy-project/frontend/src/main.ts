// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\main.ts
// 功能: 主入口

import { createApp } from "vue";
import { createPinia } from "pinia";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";

import App from "./App.vue";
import router from "./router";

createApp(App)
  .use(createPinia())
  .use(router)
  .use(ElementPlus)
  .mount("#app");

