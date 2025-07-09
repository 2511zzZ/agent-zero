# 新 UI 端口启动方案

## 概述

为了不影响现有的 WebUI 系统，新的 React + React Flow UI 将在独立的端口上运行，与原有系统并行存在。

## 部署架构

### 1. 端口分配

```
┌─────────────────────────────────────────────────────┐
│                Backend Services                    │
│                                                     │
│  ┌─────────────────────────────────────────────────┐ │
│  │           Flask API Server                      │ │
│  │         (run_ui.py 启动)                         │ │
│  │            Port: 8080                           │ │
│  │                                                 │ │
│  │  API Routes:                                    │ │
│  │  - /message_async                               │ │
│  │  - /poll                                        │ │
│  │  - /flowchart_* (新增)                          │ │
│  │  - /project_* (新增)                            │ │
│  │  - 其他现有 API                                  │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────┐
│                Frontend Services                   │
│                                                     │
│  ┌─────────────────────┐    ┌─────────────────────┐ │
│  │    旧 WebUI         │    │   新 React UI       │ │
│  │   (静态文件服务)      │    │  (Vite 开发服务器)   │ │
│  │   Port: 8080       │    │   Port: 3000        │ │
│  │                    │    │                     │ │
│  │  - index.html      │    │  - React App        │ │
│  │  - index.js        │    │  - TypeScript       │ │
│  │  - board.html      │    │  - React Flow       │ │
│  │  - CSS/JS 文件     │    │  - Ant Design       │ │
│  └─────────────────────┘    └─────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### 2. 启动脚本设计

#### 2.1 开发环境启动

**方案A: 独立启动脚本**

```bash
# 启动脚本 1: start_legacy_ui.sh
#!/bin/bash
echo "Starting Legacy WebUI..."
cd /path/to/agent-zero
python run_ui.py --port 8080
```

```bash
# 启动脚本 2: start_new_ui.sh
#!/bin/bash
echo "Starting New React UI..."
cd /path/to/agent-zero/ui-react
npm run dev
```

**方案B: 统一启动脚本**

```bash
# 启动脚本: start_ui.sh
#!/bin/bash

# 检查参数
if [ "$1" = "legacy" ]; then
    echo "Starting Legacy WebUI on port 8080..."
    cd /path/to/agent-zero
    python run_ui.py --port 8080
elif [ "$1" = "new" ]; then
    echo "Starting New React UI on port 3000..."
    cd /path/to/agent-zero/ui-react
    npm run dev
elif [ "$1" = "both" ]; then
    echo "Starting both UIs..."
    # 后台启动 Legacy UI
    cd /path/to/agent-zero
    python run_ui.py --port 8080 &
    LEGACY_PID=$!
    
    # 前台启动 New UI
    cd /path/to/agent-zero/ui-react
    npm run dev &
    NEW_PID=$!
    
    echo "Legacy UI PID: $LEGACY_PID"
    echo "New UI PID: $NEW_PID"
    
    # 等待任一进程结束
    wait
else
    echo "Usage: $0 [legacy|new|both]"
    echo "  legacy: Start legacy WebUI (port 8080)"
    echo "  new: Start new React UI (port 3000)"
    echo "  both: Start both UIs"
fi
```

#### 2.2 生产环境部署

**Docker Compose 配置**

```yaml
version: '3.8'

services:
  agent-zero-backend:
    build: .
    ports:
      - "8080:8080"
    environment:
      - FLASK_ENV=production
    command: python run_ui.py --port 8080
    
  agent-zero-ui-legacy:
    build: .
    depends_on:
      - agent-zero-backend
    # 由 backend 提供静态文件服务
    
  agent-zero-ui-new:
    build:
      context: ./ui-react
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8080
    depends_on:
      - agent-zero-backend
```

**Nginx 反向代理配置**

```nginx
server {
    listen 80;
    server_name agent-zero.example.com;

    # 新 UI 路由
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 旧 UI 路由
    location /legacy {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API 路由
    location /api {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. 新 UI 项目结构

```
agent-zero/
├── ui-react/                    # 新 React UI 项目
│   ├── public/                  # 静态资源
│   ├── src/                     # 源代码
│   │   ├── components/          # 组件
│   │   ├── pages/               # 页面
│   │   ├── stores/              # 状态管理
│   │   ├── utils/               # 工具函数
│   │   ├── types/               # 类型定义
│   │   └── App.tsx              # 主应用
│   ├── package.json             # 依赖配置
│   ├── vite.config.ts           # Vite 配置
│   ├── tailwind.config.js       # Tailwind 配置
│   └── tsconfig.json            # TypeScript 配置
├── webui/                       # 原有 WebUI
├── run_ui.py                    # 后端启动脚本
├── run_new_ui.py                # 新 UI 启动脚本 (可选)
└── start_ui.sh                  # 统一启动脚本
```

### 4. 配置文件修改

#### 4.1 新增后端启动配置

**run_new_ui.py** (可选，用于自定义新 UI 的后端配置)

```python
#!/usr/bin/env python3
"""
新 UI 专用启动脚本
支持新 UI 所需的特定配置和 API 路由
"""

import argparse
from run_ui import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent Zero New UI Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--ui-type", default="new", choices=["legacy", "new"], 
                       help="UI type to serve")
    
    args = parser.parse_args()
    
    # 设置新 UI 特定的配置
    if args.ui_type == "new":
        # 启用新 UI 相关的 API 路由
        # 设置 CORS 配置支持 localhost:3000
        pass
    
    main(args)
```

#### 4.2 Vite 配置

**ui-react/vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          antd: ['antd'],
          reactflow: ['reactflow']
        }
      }
    }
  }
})
```

#### 4.3 环境变量配置

**.env.development**

```bash
# 开发环境配置
VITE_API_BASE_URL=http://localhost:8080
VITE_WS_BASE_URL=ws://localhost:8080
VITE_UI_TYPE=new
```

**.env.production**

```bash
# 生产环境配置
VITE_API_BASE_URL=https://api.agent-zero.com
VITE_WS_BASE_URL=wss://api.agent-zero.com
VITE_UI_TYPE=new
```

### 5. API 跨域配置

#### 5.1 Flask CORS 配置

**修改 run_ui.py**

```python
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # 配置 CORS 支持新 UI
    CORS(app, origins=[
        "http://localhost:3000",  # 新 UI 开发服务器
        "http://localhost:8080",  # 旧 UI
        "https://agent-zero.com", # 生产环境
    ])
    
    # 其他配置...
    return app
```

#### 5.2 API 路由前缀

```python
# 为新 UI 添加专用 API 路由前缀
@app.route('/api/v2/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_v2_proxy(path):
    """新 UI 专用 API 路由"""
    return handle_api_request(path, version='v2')

@app.route('/api/v1/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_v1_proxy(path):
    """旧 UI 兼容 API 路由"""
    return handle_api_request(path, version='v1')
```

### 6. 开发工作流

#### 6.1 开发阶段

```bash
# 终端 1: 启动后端服务
cd agent-zero
python run_ui.py --port 8080

# 终端 2: 启动新 UI 开发服务器
cd agent-zero/ui-react
npm run dev

# 访问方式:
# 旧 UI: http://localhost:8080
# 新 UI: http://localhost:3000
```

#### 6.2 测试阶段

```bash
# 统一启动脚本
./start_ui.sh both

# 或者使用 Docker Compose
docker-compose up -d
```

#### 6.3 部署阶段

```bash
# 构建新 UI
cd ui-react
npm run build

# 部署到生产环境
docker-compose -f docker-compose.prod.yml up -d
```

### 7. 迁移策略

#### 7.1 渐进式迁移

1. **Phase 1**: 两套 UI 并行运行
2. **Phase 2**: 逐步迁移用户到新 UI
3. **Phase 3**: 收集反馈并优化
4. **Phase 4**: 考虑是否废弃旧 UI

#### 7.2 用户选择机制

```python
# 在后端添加 UI 选择逻辑
@app.route('/')
def index():
    ui_preference = request.cookies.get('ui_preference', 'legacy')
    
    if ui_preference == 'new':
        return redirect('http://localhost:3000')
    else:
        return serve_legacy_ui()

@app.route('/switch-ui')
def switch_ui():
    current_ui = request.cookies.get('ui_preference', 'legacy')
    new_ui = 'new' if current_ui == 'legacy' else 'legacy'
    
    response = make_response(redirect('/'))
    response.set_cookie('ui_preference', new_ui)
    return response
```

### 8. 监控和日志

#### 8.1 访问日志分离

```python
import logging

# 创建不同的日志处理器
legacy_logger = logging.getLogger('legacy_ui')
new_ui_logger = logging.getLogger('new_ui')

# 记录不同 UI 的访问情况
@app.before_request
def log_request():
    if request.endpoint and request.endpoint.startswith('new_ui'):
        new_ui_logger.info(f"New UI request: {request.method} {request.path}")
    else:
        legacy_logger.info(f"Legacy UI request: {request.method} {request.path}")
```

#### 8.2 性能监控

```typescript
// 新 UI 性能监控
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric: any) {
  // 发送性能指标到后端
  fetch('/api/metrics', {
    method: 'POST',
    body: JSON.stringify(metric)
  });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

## 总结

这个方案确保了：

1. **隔离性**: 新旧 UI 在不同端口运行，互不干扰
2. **兼容性**: 现有用户可以继续使用旧 UI
3. **可扩展性**: 支持逐步迁移和功能测试
4. **可维护性**: 清晰的项目结构和启动流程
5. **生产就绪**: 支持 Docker 和 Nginx 部署

通过这种方式，可以安全地引入新 UI，同时保持现有系统的稳定性。