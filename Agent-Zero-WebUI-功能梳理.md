# Agent Zero WebUI 功能梳理文档

## 概述

本文档梳理了 Agent Zero 现有 WebUI 的功能模块和 API 接口，用于指导新的 React + React Flow UI 实现。

## 1. 核心聊天功能

### 1.1 前端模块
- **文件**: `webui/index.html`, `webui/index.js`, `webui/js/messages.js`
- **功能描述**:
  - 实时消息发送和接收
  - 消息历史记录显示
  - 支持多种消息类型（用户、Agent、工具、错误等）
  - Markdown 渲染支持
  - 数学公式渲染（KaTeX）
  - 消息复制功能
  - 消息重新生成功能

### 1.2 API 接口
- **消息发送**: `POST /message` 或 `POST /message_async`
- **消息轮询**: `POST /poll`
- **数据格式**:
  ```json
  {
    "text": "消息内容",
    "context": "context_id",
    "message_id": "msg_id",
    "attachments": ["file1", "file2"]
  }
  ```

## 2. 文件管理功能

### 2.1 前端模块
- **文件**: `webui/js/file_browser.js`, `webui/css/file_browser.css`
- **功能描述**:
  - 文件/文件夹浏览
  - 文件上传（拖拽支持）
  - 文件下载
  - 文件删除
  - 文件预览（图片）
  - 文件信息查看

### 2.2 API 接口
- **文件列表**: `GET /get_work_dir_files`
- **文件信息**: `POST /file_info`
- **文件上传**: `POST /upload`
- **文件下载**: `GET /download_work_dir_file`
- **文件删除**: `POST /delete_work_dir_file`

## 3. 设置管理功能

### 3.1 前端模块
- **文件**: `webui/js/settings.js`, `webui/css/settings.css`
- **功能描述**:
  - 系统设置配置
  - 主题切换（亮色/暗色）
  - 语言设置
  - API 密钥管理
  - 代理设置
  - 模型配置

### 3.2 API 接口
- **获取设置**: `POST /settings_get`
- **保存设置**: `POST /settings_set`

## 4. 历史记录功能

### 4.1 前端模块
- **文件**: `webui/js/history.js`, `webui/css/history.css`
- **功能描述**:
  - 聊天历史记录查看
  - 历史记录搜索
  - 历史记录导出
  - 历史记录删除

### 4.2 API 接口
- **历史记录**: `POST /history_get`
- **聊天导出**: `POST /chat_export`
- **聊天加载**: `POST /chat_load`
- **聊天删除**: `POST /chat_remove`
- **聊天重置**: `POST /chat_reset`

## 5. 任务调度功能

### 5.1 前端模块
- **文件**: `webui/js/scheduler.js`
- **功能描述**:
  - 任务列表显示
  - 任务创建和编辑
  - 任务状态管理
  - 任务执行控制
  - 任务计划设置

### 5.2 API 接口
- **任务创建**: `POST /scheduler_task_create`
- **任务列表**: `POST /scheduler_tasks_list`
- **任务更新**: `POST /scheduler_task_update`
- **任务删除**: `POST /scheduler_task_delete`
- **任务执行**: `POST /scheduler_task_run`
- **调度器心跳**: `POST /scheduler_tick`

## 6. Board 可视化功能

### 6.1 前端模块
- **文件**: `webui/board.html`
- **功能描述**:
  - 无限画布设计
  - 节点拖拽和编辑
  - 节点类型管理（计划、里程碑、交付物、笔记）
  - 节点连接和关系
  - 实时聊天面板集成

### 6.2 API 接口
- **获取看板**: `POST /board_get`
- **更新看板**: `POST /board_update`
- **看板轮询**: `POST /board_poll`
- **看板路由**: `POST /board_route`

## 7. 语音功能

### 7.1 前端模块
- **文件**: `webui/js/speech.js`, `webui/css/speech.css`
- **功能描述**:
  - 语音输入识别
  - 文本转语音播放
  - 语音控制功能
  - 语音设置管理

### 7.2 API 接口
- **语音转文本**: `POST /transcribe`

## 8. MCP 服务器管理

### 8.1 前端模块
- **文件**: `webui/components/settings/mcp/`
- **功能描述**:
  - MCP 服务器状态监控
  - 服务器配置管理
  - 服务器日志查看
  - 服务器启动/停止控制

### 8.2 API 接口
- **服务器状态**: `POST /mcp_servers_status`
- **服务器配置**: `POST /mcp_servers_apply`
- **服务器详情**: `POST /mcp_server_get_detail`
- **服务器日志**: `POST /mcp_server_get_log`

## 9. 备份恢复功能

### 9.1 前端模块
- **文件**: `webui/components/settings/backup/`
- **功能描述**:
  - 系统备份创建
  - 备份文件管理
  - 备份恢复操作
  - 备份预览和检查

### 9.2 API 接口
- **创建备份**: `POST /backup_create`
- **获取默认设置**: `POST /backup_get_defaults`
- **备份检查**: `POST /backup_inspect`
- **备份预览**: `POST /backup_preview_grouped`
- **备份恢复**: `POST /backup_restore`
- **恢复预览**: `POST /backup_restore_preview`

## 10. 系统控制功能

### 10.1 前端模块
- **功能描述**:
  - 系统暂停/恢复
  - 系统重启
  - 状态监控
  - 推送通知

### 10.2 API 接口
- **健康检查**: `GET /health`
- **CSRF Token**: `POST /csrf_token`
- **暂停/恢复**: `POST /pause`
- **重启**: `POST /restart`
- **推送**: `POST /nudge`

## 11. 附加功能

### 11.1 前端模块
- **隧道管理**: `webui/css/tunnel.css`
- **通知系统**: `webui/css/toast.css`
- **模态框**: `webui/css/modals.css`

### 11.2 API 接口
- **隧道管理**: `POST /tunnel`
- **图像获取**: `POST /image_get`
- **知识导入**: `POST /import_knowledge`
- **RFC 处理**: `POST /rfc`
- **上下文窗口**: `POST /ctx_window_get`

## 12. 技术架构特点

### 12.1 前端技术栈
- **框架**: 原生 JavaScript + Alpine.js
- **模块化**: ES6 模块系统
- **组件化**: 自定义组件系统 (x-component)
- **状态管理**: Alpine.js 响应式状态
- **样式**: 原生 CSS + CSS 变量（主题支持）

### 12.2 API 架构
- **框架**: Flask + 异步处理
- **认证**: Basic Auth + API Key + CSRF
- **安全**: 回环地址限制、文件安全处理
- **数据格式**: JSON + multipart/form-data
- **错误处理**: 统一异常处理机制

## 13. 实时通信机制

### 13.1 轮询系统
- **短轮询**: 活跃时 25ms 间隔
- **长轮询**: 空闲时 250ms 间隔
- **自适应**: 根据活动状态调整频率

### 13.2 上下文管理
- 支持多个聊天上下文
- 上下文切换和状态保持
- 任务和聊天的分离管理

---

## 新 UI 实现方案（更新版）

基于用户反馈和最新需求，重新设计 React + React Flow UI 的实现方案：

### 核心架构调整

#### 1. 三层架构设计
```
┌─────────────────────────────────────────────────────┐
│                Layer 1: Project 管理                │
│  - 项目列表页面（首页）                               │
│  - 项目创建、删除、重命名                            │
│  - 项目状态管理                                      │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│            Layer 2: 画板 + 聊天界面                  │
│  ┌─────────────────────┐  ┌─────────────────────────┐ │
│  │   React Flow 画板   │  │    聊天对话侧边栏        │ │
│  │   (主要区域)        │  │                         │ │
│  │                     │  │  - 消息历史记录          │ │
│  │                     │  │  - 消息发送              │ │
│  │                     │  │  - Markdown 渲染         │ │
│  │                     │  │  - 消息复制              │ │
│  └─────────────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

#### 2. 端口分离设计
- **旧 WebUI**: 保持在原端口运行（如 8080）
- **新 React UI**: 在新端口运行（如 3000）
- **API 层**: 两套 UI 共享同一套后端 API

### 功能实现优先级

#### Phase 1: 核心功能（必须实现）

**1. 聊天对话功能**
- **完全复用现有 API**：`/message_async`, `/poll`
- **消息发送和接收**：支持文本消息的实时发送和接收
- **消息历史记录**：显示完整的对话历史
- **Markdown 渲染**：支持代码块、链接、格式化文本等
- **消息复制**：方便用户复制 Agent 回复
- **New Chat**：创建新的对话会话

**2. React Flow 画板功能**
- **重新设计 API 和 Tools**：不复用现有 board API
- **Agent 生成 React Flow JSON**：直接生成 React Flow 配置
- **无限画布**：基于 React Flow 的可拖拽画布
- **节点管理**：创建、编辑、删除节点
- **节点类型**：计划、里程碑、交付物、笔记等不同类型
- **节点连接**：节点间的连线关系
- **画板持久化**：保存和加载画板状态

**3. Project 管理功能**
- **项目列表页面**：作为应用首页
- **项目 CRUD**：创建、删除、重命名项目
- **项目状态管理**：活跃、归档状态
- **项目级别的画板和聊天历史**

#### Phase 2: 辅助功能（可选实现）

**4. 基础系统控制**
- **暂停/恢复**：控制 Agent 的执行状态
- **状态显示**：显示系统运行状态
- **相关 API**：`/pause`, `/restart`, `/health`

### 技术栈选择

- **前端框架**：React 18+ with TypeScript
- **构建工具**：Vite
- **状态管理**：Zustand
- **UI 组件库**：Ant Design
- **画板组件**：React Flow
- **样式方案**：Tailwind CSS
- **路由**：React Router
- **HTTP 客户端**：Axios

### React Flow 集成策略

#### 1. Agent 工具简化
- **不提供复杂的 FlowchartTools**
- **Agent 直接生成 React Flow JSON 配置**
- **前端解析 JSON 并渲染到 React Flow**

#### 2. 数据流设计
```
Agent 消息 → React Flow JSON → 前端解析 → React Flow 渲染
```

#### 3. JSON 配置格式
```json
{
  "action": "update_flowchart",
  "data": {
    "nodes": [
      {
        "id": "1",
        "type": "plan",
        "position": { "x": 100, "y": 100 },
        "data": {
          "title": "项目规划",
          "content": "制定项目的整体规划和目标"
        }
      }
    ],
    "edges": [
      {
        "id": "e1-2",
        "source": "1",
        "target": "2",
        "type": "dependency"
      }
    ]
  }
}
```

### 部署方案

#### 1. 开发环境
```bash
# 新 UI 开发服务器
cd agent-zero-ui
npm run dev  # 运行在 localhost:3000

# 原 WebUI 服务器
python run_ui.py  # 运行在 localhost:8080
```

#### 2. 生产环境
- **反向代理配置**：Nginx 配置不同路径
- **静态文件服务**：新 UI 打包后的静态文件
- **API 代理**：新 UI 的 API 请求代理到后端

### 暂不实现的功能

#### 1. 文件附件功能
- **文件上传下载**：Phase 1 暂不实现
- **文件预览**：Phase 1 暂不实现

#### 2. 系统配置功能
- **API 密钥管理**：属于系统配置
- **模型配置**：属于开发者配置
- **MCP 服务器管理**：属于系统管理功能

#### 3. 高级管理功能
- **任务调度管理**：属于系统级功能
- **备份恢复**：属于系统管理功能
- **语音功能**：Phase 1 暂不实现

### 开发路线图

#### Phase 1（核心功能）
1. 项目脚手架搭建
2. Project 管理页面
3. 基础聊天功能
4. React Flow 画板集成
5. Agent JSON 配置解析

#### Phase 2（功能完善）
1. 文件上传下载
2. 语音功能
3. 系统控制功能
4. 性能优化

#### Phase 3（体验优化）
1. 响应式设计
2. 快捷键支持
3. 用户体验优化
4. 错误处理完善

这个方案专注于核心功能，通过简化的 Agent 工具设计和独立的端口部署，确保不影响现有系统的同时提供更好的用户体验。