# React Flow 集成与实现计划

## 项目概述

基于用户需求，重新设计 Agent Zero 的 UI 系统，采用 React + React Flow 技术栈，实现 Project 管理 + 画板 + 聊天的三层架构。

## 架构设计

### 1. 三层架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                        Layer 1: Project 管理                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Project List (首页)                                         │ │
│  │  - 项目列表展示                                               │ │
│  │  - 项目创建、删除、重命名                                      │ │
│  │  - 项目状态管理                                               │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Layer 2: 画板 + 聊天界面                      │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐ │
│  │      React Flow 画板        │  │        聊天侧边栏            │ │
│  │                             │  │                             │ │
│  │  - 无限画布                  │  │                           │ │
│  │  - 节点管理                  │  │  - 消息发送                  │ │
│  │  - 连线管理                  │  │  - Markdown 渲染             │ │
│  │  - Agent 生成内容渲染        │  │                            │ │
│  │                             │  │                           │ │
│  └─────────────────────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Layer 3: API 和数据层                        │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  聊天 API (复用现有)     │  画板 API (重新设计)                │ │
│  │  - /message_async        │  - /flowchart_*                   │ │
│  │  - /poll                │  - /project_*                     │ │
│  │  - /chat_*              │  - React Flow 描述语言             │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 2. 技术栈选择

- **前端框架**: React 18+ with TypeScript
- **构建工具**: Vite
- **状态管理**: Zustand
- **UI 组件库**: Ant Design
- **画板组件**: React Flow
- **样式方案**: Tailwind CSS
- **路由**: React Router
- **HTTP 客户端**: Axios

## 数据结构设计

### 1. Project 数据结构

```typescript
interface Project {
  id: string;                    // 项目唯一标识
  name: string;                  // 项目名称
  description?: string;          // 项目描述
  createdAt: string;            // 创建时间
  updatedAt: string;            // 更新时间
  flowchart: FlowchartData;     // 画板数据
  chatHistory: ChatMessage[];   // 聊天历史
  status: 'active' | 'archived'; // 项目状态
}
```

### 2. React Flow 数据结构

```typescript
interface FlowchartData {
  nodes: FlowNode[];            // 节点数组
  edges: FlowEdge[];            // 边数组
  viewport: Viewport;           // 视窗状态
  version: number;              // 版本号
}

interface FlowNode {
  id: string;                   // 节点 ID
  type: 'plan' | 'milestone' | 'deliverable' | 'note' | 'chat';
  position: { x: number; y: number; };
  data: {
    title: string;              // 节点标题
    content: string;            // 节点内容
    status?: 'pending' | 'in_progress' | 'completed';
    priority?: 'low' | 'medium' | 'high';
    assignee?: string;          // 负责人
    dueDate?: string;           // 截止日期
    metadata?: Record<string, any>; // 元数据
  };
  style?: React.CSSProperties;
  className?: string;
}

interface FlowEdge {
  id: string;                   // 边 ID
  source: string;               // 源节点 ID
  target: string;               // 目标节点 ID
  type: 'dependency' | 'sequence' | 'reference';
  data: {
    label?: string;             // 边标签
    weight?: number;            // 权重
    metadata?: Record<string, any>;
  };
  style?: React.CSSProperties;
}
```

### 3. Chat 数据结构（复用现有）

```typescript
interface ChatMessage {
  id: string;
  type: 'user' | 'agent' | 'system' | 'tool' | 'error';
  content: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

interface ChatContext {
  id: string;
  messages: ChatMessage[];
  projectId: string;
  createdAt: string;
  updatedAt: string;
}
```

## React Flow 描述语言设计

### 1. 设计原则

- **声明式**: Agent 通过声明式语法描述画板结构
- **类型安全**: 基于 TypeScript 的类型系统
- **易于理解**: 语法简洁，易于 Agent 学习和生成
- **可扩展**: 支持自定义节点类型和属性

### 2. 描述语言语法

```typescript
// Agent 生成的描述语言示例
interface FlowchartDescription {
  action: 'create' | 'update' | 'delete' | 'connect' | 'disconnect';
  target: 'node' | 'edge' | 'flowchart';
  data: any;
}

// 创建节点
const createNodeDescription: FlowchartDescription = {
  action: 'create',
  target: 'node',
  data: {
    id: 'node-1',
    type: 'plan',
    position: { x: 100, y: 100 },
    data: {
      title: '项目规划',
      content: '制定项目的整体规划和目标',
      status: 'pending',
      priority: 'high'
    }
  }
};

// 创建连接
const createEdgeDescription: FlowchartDescription = {
  action: 'create',
  target: 'edge',
  data: {
    id: 'edge-1',
    source: 'node-1',
    target: 'node-2',
    type: 'dependency',
    data: {
      label: '前置依赖'
    }
  }
};
```

### 3. Agent JSON 配置生成设计

```typescript
// Agent 直接生成 React Flow JSON 配置，不使用复杂工具
interface FlowchartMessage {
  action: 'update_flowchart' | 'clear_flowchart' | 'get_flowchart';
  data: {
    nodes?: FlowNode[];
    edges?: FlowEdge[];
    viewport?: {
      x: number;
      y: number;
      zoom: number;
    };
  };
}

// Agent 生成的标准 React Flow JSON 示例
const flowchartUpdate: FlowchartMessage = {
  action: 'update_flowchart',
  data: {
    nodes: [
      {
        id: '1',
        type: 'plan',
        position: { x: 100, y: 100 },
        data: {
          title: '项目规划',
          content: '制定项目的整体规划和目标',
          status: 'pending',
          priority: 'high'
        }
      },
      {
        id: '2',
        type: 'milestone',
        position: { x: 300, y: 100 },
        data: {
          title: '里程碑1',
          content: '完成需求分析',
          status: 'in_progress',
          dueDate: '2024-01-15'
        }
      }
    ],
    edges: [
      {
        id: 'e1-2',
        source: '1',
        target: '2',
        type: 'dependency',
        data: {
          label: '前置依赖'
        }
      }
    ]
  }
};

// 简化的 Agent 工具接口
interface FlowchartTool {
  // 仅提供一个工具：生成 React Flow JSON 配置
  generateFlowchartConfig(description: string): Promise<FlowchartMessage>;
}
```

## API 设计

### 1. Project 管理 API

```typescript
// GET /api/projects - 获取项目列表
interface GetProjectsResponse {
  projects: Project[];
  total: number;
  page: number;
  pageSize: number;
}

// POST /api/projects - 创建项目
interface CreateProjectRequest {
  name: string;
  description?: string;
}

// PUT /api/projects/:id - 更新项目
interface UpdateProjectRequest {
  name?: string;
  description?: string;
  status?: 'active' | 'archived';
}

// DELETE /api/projects/:id - 删除项目
```

### 2. 画板 API

```typescript
// GET /api/projects/:id/flowchart - 获取画板数据
interface GetFlowchartResponse {
  flowchart: FlowchartData;
  version: number;
}

// POST /api/projects/:id/flowchart/update - 更新画板数据
interface UpdateFlowchartRequest {
  description: FlowchartDescription;
  version: number;
}

// POST /api/projects/:id/flowchart/batch - 批量更新画板
interface BatchUpdateFlowchartRequest {
  descriptions: FlowchartDescription[];
  version: number;
}
```

### 3. 聊天 API（复用现有）

```typescript
// 复用现有的聊天 API，但需要扩展 context 参数
interface ChatRequest {
  text: string;
  context: string;           // 格式: project_id
  projectId: string;         // 新增：项目 ID
  flowchartContext?: FlowchartData; // 新增：画板上下文
}
```

## 组件设计

### 1. 页面组件

```typescript
// 项目列表页面
const ProjectListPage: React.FC = () => {
  // 项目列表逻辑
};

// 项目详情页面（画板 + 聊天）
const ProjectDetailPage: React.FC = () => {
  // 画板和聊天集成逻辑
};
```

### 2. 画板组件

```typescript
// 主画板组件
const FlowchartCanvas: React.FC<{
  projectId: string;
  onNodeClick: (node: FlowNode) => void;
  onEdgeClick: (edge: FlowEdge) => void;
}> = ({ projectId, onNodeClick, onEdgeClick }) => {
  // React Flow 集成逻辑
};

// 自定义节点组件
const CustomNode: React.FC<{
  data: FlowNode['data'];
  type: FlowNode['type'];
}> = ({ data, type }) => {
  // 节点渲染逻辑
};
```

### 3. 聊天组件

```typescript
// 聊天侧边栏组件
const ChatSidebar: React.FC<{
  projectId: string;
  flowchartContext: FlowchartData;
}> = ({ projectId, flowchartContext }) => {
  // 聊天逻辑，复用现有组件
};
```

## 项目结构设计

### 1. 文件夹结构

```
agent-zero/
├── webui/                       # 现有的旧 WebUI
│   ├── index.html
│   ├── index.js
│   └── ...
├── ui-react/                    # 新的 React UI 项目
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/          # 通用组件
│   │   │   ├── Chat/           # 聊天组件
│   │   │   ├── Flowchart/      # 画板组件
│   │   │   ├── Project/        # 项目组件
│   │   │   └── Common/         # 通用组件
│   │   ├── pages/              # 页面组件
│   │   │   ├── ProjectList/    # 项目列表页
│   │   │   └── ProjectDetail/  # 项目详情页
│   │   ├── stores/             # Zustand 状态管理
│   │   ├── services/           # API 服务
│   │   ├── types/              # TypeScript 类型
│   │   ├── utils/              # 工具函数
│   │   ├── hooks/              # 自定义 Hooks
│   │   └── App.tsx             # 主应用
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── README.md
├── python/                      # 现有的后端代码
├── run_ui.py                    # 现有的启动脚本
└── README.md
```

### 2. 独立项目配置

新的 React UI 作为完全独立的前端项目，可以单独部署和维护。

## 实现步骤（更新版）

### Phase 1: 基础架构搭建

1. **项目初始化**
   - 在 `ui-react/` 目录创建 React + TypeScript + Vite 项目
   - 配置 Tailwind CSS + Ant Design
   - 设置 Zustand 状态管理
   - 配置路由和基础布局
   - 设置 API 代理到后端（端口 8080）

2. **数据结构定义**
   - 定义 TypeScript 接口
   - 创建状态管理 store
   - 设计新的 API 接口规范（Project 和 Flowchart）

3. **基础组件开发**
   - 项目列表页面（首页）
   - 项目卡片组件
   - 布局组件
   - 导航组件

### Phase 2: 聊天功能集成

1. **聊天 API 适配**
   - **完全复用**现有的 `/message_async` 和 `/poll` API
   - 扩展 context 参数支持项目 ID 格式
   - 实现实时轮询机制

2. **聊天组件开发**
   - 消息列表组件
   - 消息输入组件
   - Markdown 渲染组件
   - 消息复制功能
   - New Chat 功能

3. **聊天状态管理**
   - 消息历史存储
   - 实时更新机制
   - 错误处理

### Phase 3: React Flow 画板实现

1. **React Flow 集成**
   - 安装和配置 React Flow
   - 创建基础画板组件
   - 实现节点和边的基本操作

2. **自定义节点开发**
   - 计划节点组件
   - 里程碑节点组件
   - 交付物节点组件
   - 笔记节点组件

3. **画板交互功能**
   - 节点拖拽和连接
   - 右键菜单
   - 选择和编辑
   - 缩放和平移

### Phase 4: Agent 集成

1. **描述语言解析**
   - 实现描述语言解析器
   - 画板状态更新机制
   - 版本控制和冲突处理

2. **Agent Tools 开发**
   - 实现画板操作工具
   - Agent 权限控制
   - 操作历史记录

3. **实时同步**
   - 画板状态实时同步
   - 聊天和画板联动
   - 性能优化

### Phase 5: 完善和优化

1. **用户体验优化**
   - 加载状态处理
   - 错误提示和恢复
   - 快捷键支持
   - 响应式设计

2. **性能优化**
   - 虚拟化渲染
   - 状态管理优化
   - 网络请求优化
   - 内存管理

3. **测试和部署**
   - 单元测试
   - 集成测试
   - 性能测试
   - 部署配置

## 技术难点和解决方案

### 1. 聊天和画板状态同步

**难点**: 聊天过程中 Agent 修改画板，需要实时同步状态

**解决方案**:
- 使用 WebSocket 或长轮询实现实时通信
- 设计状态冲突解决机制
- 实现乐观更新和回滚机制

### 2. React Flow 性能优化

**难点**: 大量节点和边的渲染性能问题

**解决方案**:
- 使用 React.memo 优化组件渲染
- 实现虚拟化渲染
- 使用 useCallback 和 useMemo 优化计算
- 采用 Zustand 进行状态管理

### 3. Agent 描述语言设计

**难点**: 设计易于 Agent 理解和生成的描述语言

**解决方案**:
- 采用声明式语法
- 提供丰富的类型定义
- 设计清晰的操作语义
- 提供详细的示例和文档

### 4. 数据持久化和版本控制

**难点**: 画板数据的持久化和版本管理

**解决方案**:
- 实现增量更新机制
- 设计版本控制系统
- 支持操作历史回滚
- 实现自动保存功能

## 总结

这个实现计划基于对 React Flow 的深入调研和用户需求的准确理解，设计了一个完整的三层架构系统。通过复用现有的聊天 API 和重新设计画板功能，既保证了开发效率，又实现了功能创新。

核心创新点包括：
1. **Project 管理**: 引入项目概念，提供更好的组织结构
2. **React Flow 集成**: 基于专业画板库实现高质量可视化
3. **Agent 描述语言**: 让 Agent 能够直接操作画板内容
4. **实时同步**: 聊天和画板的无缝集成

这个计划为后续的开发提供了清晰的路线图和技术指导。