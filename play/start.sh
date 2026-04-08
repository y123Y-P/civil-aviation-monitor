# 文件名: Users\24704\Desktop\civil-aviation-monitor-main\play\start.sh
# 功能: 模块功能实现

#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 -m http.server 3000
