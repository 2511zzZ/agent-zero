# Agent Zero React UI 实现计划和技术方案

## 当前状态分析

### 已实现功能
1. ✅ **基础项目结构**：React + TypeScript + Vite + Tailwind CSS + Ant Design
2. ✅ **后端 Project API**：project_create.py、project_get.py、project_list.py 等已实现
3. ✅ **前端 API 服务层**：services/api.ts 已定义接口
4. ✅ **基础类型定义**：types/index.ts 已定义数据结构
5. ✅ **路由配置**：React Router 已配置
6. ✅ **API 代理配置**：Vite 配置代理到 localhost:50080

### 主要问题
1. ❌ **Project API 调用错误**：`/project_get` 返回 `{"success": false, "error": "Project not found"}`
2. ❌ **聊天功能未实现**：缺少聊天组件和实时轮询
3. ❌ **React Flow 未集成**：缺少画板组件实现
4. ❌ **UI 设计不完整**：需要按 Figma 设计重新实现

## 执行计划

### Phase 1: 修复 Project API 问题 (优先级：高)

#### 1.1 问题诊断
- **问题原因分析**：
  - 前端 API 路径不匹配：前端调用 `/api/project_get`，但后端注册为 `/project_get`
  - 可能的 CORS 问题
  - 请求格式不匹配

#### 1.2 解决方案
1. **修复 API 路径映射**：
   - 检查 Vite 代理配置
   - 确保前端 API 调用路径正确
   - 验证后端 API 注册路径

2. **数据格式校验**：
   - 确保请求数据格式符合后端期望
   - 检查响应数据格式

3. **错误处理优化**：
   - 添加详细的错误日志
   - 改进错误提示信息

### Phase 2: 实现聊天功能 (优先级：高)

#### 2.1 技术方案
- **完全复用现有 API**：`/message_async` 和 `/poll`
- **实时轮询机制**：参考原 WebUI 的轮询逻辑
- **项目级上下文**：context 格式为 `project_{project_id}`

#### 2.2 实现步骤
1. **创建聊天组件**：
   - `ChatSidebar.tsx`：聊天侧边栏容器
   - `ChatMessageList.tsx`：消息列表组件
   - `ChatInput.tsx`：消息输入组件
   - `ChatMessage.tsx`：单个消息组件

2. **实现状态管理**：
   - 扩展 `useChatStore.ts`
   - 添加消息历史管理
   - 实现实时轮询逻辑

3. **Markdown 渲染**：
   - 集成 `react-markdown`
   - 代码高亮支持
   - 数学公式渲染

### Phase 3: 实现 React Flow 画板功能 (优先级：高)

#### 3.1 技术方案
- **使用 React Flow 11.x**：已在 package.json 中安装
- **自定义节点类型**：Plan、Milestone、Deliverable、Note
- **Agent 集成**：通过消息格式接收画板更新

#### 3.2 实现步骤
1. **创建画板组件**：
   - `FlowchartCanvas.tsx`：主画板组件
   - `nodes/`：自定义节点组件目录
     - `PlanNode.tsx`
     - `MilestoneNode.tsx`
     - `DeliverableNode.tsx`
     - `NoteNode.tsx`

2. **画板状态管理**：
   - 扩展 `useFlowchartStore.ts`
   - 节点和边的管理
   - 实时同步逻辑

3. **Agent 描述语言**：
   - Agent 直接生成 React Flow JSON
   - 前端解析并渲染到画板

### Phase 4: UI 设计重新实现 (优先级：中)

#### 4.1 设计要求
基于用户提供的两张 Figma 设计图：

1. **项目列表页面**：
   - 卡片式布局，类似 Figma Projects 页面
   - "Create New Project" 创建按钮
   - 项目卡片展示缩略图、标题、更新时间
   - 网格布局，响应式设计

2. **项目详情页面**：
   - 左侧：React Flow 画板（主要区域）
   - 右侧：聊天侧边栏
   - 顶部：项目标题和基础控制
   - 类似 Figma 编辑器的布局

#### 4.2 实现步骤
1. **重新设计项目列表页**：
   - 使用 Ant Design Card 组件
   - 实现网格布局
   - 添加项目缩略图生成

2. **重新设计项目详情页**：
   - 采用分割面板布局
   - 画板区域占主要空间
   - 聊天侧边栏可折叠

3. **统一设计系统**：
   - 定义主题色彩
   - 统一字体和间距
   - 响应式设计

## 技术实现细节

### 1. 修复 Project API 问题

#### 1.1 检查 API 路径问题
```typescript
// 前端当前调用路径
const response = await api.post('/project_get', { project_id: id });

// 需要确认的路径：
// Option 1: 如果后端路由为 /project_get
const response = await api.post('/project_get', { project_id: id });

// Option 2: 如果需要 /api 前缀
const response = await api.post('/api/project_get', { project_id: id });
```

#### 1.2 Vite 代理配置验证
```typescript
// vite.config.ts 当前配置
proxy: {
  '/api': {
    target: 'http://localhost:50080',
    changeOrigin: true,
    secure: false,
    rewrite: (path) => path.replace(/^\/api/, ''),
  },
}
```

### 2. 聊天功能实现

#### 2.1 聊天状态管理
```typescript
// stores/useChatStore.ts
interface ChatStore {
  messages: ChatMessage[];
  isLoading: boolean;
  context: string;
  
  sendMessage: (text: string, projectId: string) => Promise<void>;
  startPolling: (context: string) => void;
  stopPolling: () => void;
}
```

#### 2.2 轮询机制
```typescript
// 参考原 WebUI 的轮询逻辑
const pollInterval = useRef<NodeJS.Timeout>();

const startPolling = (context: string) => {
  pollInterval.current = setInterval(async () => {
    try {
      const response = await chatAPI.poll({
        context,
        log_from: 0,
        timezone: 'UTC'
      });
      // 处理响应，更新消息列表
    } catch (error) {
      console.error('Polling error:', error);
    }
  }, 250); // 250ms 间隔，与原系统一致
};
```

### 3. React Flow 画板实现

#### 3.1 自定义节点组件
```typescript
// components/Flowchart/nodes/PlanNode.tsx
const PlanNode: React.FC<NodeProps> = ({ data }) => {
  return (
    <div className="plan-node">
      <div className="node-header">
        <span className="node-icon">📋</span>
        <h3>{data.title}</h3>
      </div>
      <div className="node-content">
        <p>{data.content}</p>
        {data.status && (
          <span className={`status-badge status-${data.status}`}>
            {data.status}
          </span>
        )}
      </div>
      <Handle type="source" position={Position.Right} />
      <Handle type="target" position={Position.Left} />
    </div>
  );
};
```

#### 3.2 Agent 描述语言
```typescript
// Agent 生成的标准格式
interface FlowchartUpdate {
  action: 'update_flowchart';
  data: {
    nodes: FlowNode[];
    edges: FlowEdge[];
    viewport?: { x: number; y: number; zoom: number };
  };
}

// 前端解析逻辑
const handleFlowchartUpdate = (update: FlowchartUpdate) => {
  const { nodes, edges, viewport } = update.data;
  
  setNodes(nodes);
  setEdges(edges);
  
  if (viewport) {
    setViewport(viewport);
  }
};
```

### 4. UI 设计实现

#### 4.1 项目列表页面
```typescript
// pages/ProjectList/ProjectList.tsx
const ProjectList: React.FC = () => {
  return (
    <div className="project-list-container">
      <header className="page-header">
        <h1>Projects</h1>
      </header>
      
      <div className="projects-grid">
        <Card 
          className="create-project-card"
          onClick={handleCreateProject}
        >
          <div className="create-project-content">
            <PlusOutlined className="create-icon" />
            <span>Create New Project</span>
          </div>
        </Card>
        
        {projects.map(project => (
          <ProjectCard 
            key={project.id} 
            project={project}
            onClick={() => navigate(`/project/${project.id}`)}
          />
        ))}
      </div>
    </div>
  );
};
```

#### 4.2 项目详情页面
```typescript
// pages/ProjectDetail/ProjectDetail.tsx
const ProjectDetail: React.FC = () => {
  return (
    <div className="project-detail-container">
      <header className="project-header">
        <h1>{project?.name}</h1>
        <div className="project-controls">
          {/* 项目控制按钮 */}
        </div>
      </header>
      
      <div className="project-content">
        <div className="flowchart-section">
          <FlowchartCanvas projectId={projectId} />
        </div>
        
        <div className="chat-section">
          <ChatSidebar 
            projectId={projectId}
            flowchartContext={flowchartData}
          />
        </div>
      </div>
    </div>
  );
};
```

## 实施时间表

### Week 1: 基础问题修复
- [ ] Day 1-2: 修复 Project API 调用问题
- [ ] Day 3-4: 实现基础聊天功能
- [ ] Day 5-7: 完善聊天界面和实时轮询

### Week 2: 核心功能实现
- [ ] Day 1-3: 实现 React Flow 画板基础功能
- [ ] Day 4-5: 创建自定义节点组件
- [ ] Day 6-7: 实现 Agent 描述语言解析

### Week 3: UI 设计和完善
- [ ] Day 1-3: 重新设计项目列表页面
- [ ] Day 4-5: 重新设计项目详情页面
- [ ] Day 6-7: 响应式设计和细节优化

### Week 4: 测试和优化
- [ ] Day 1-3: 功能测试和 Bug 修复
- [ ] Day 4-5: 性能优化
- [ ] Day 6-7: 文档完善和部署准备

## 风险评估

### 高风险项
1. **API 兼容性**：新旧系统 API 兼容性问题
2. **Real-time 同步**：聊天和画板的实时同步复杂度

### 中风险项
1. **React Flow 集成**：自定义节点和 Agent 集成的复杂度
2. **性能问题**：大量节点时的渲染性能

### 低风险项
1. **UI 设计**：主要是 CSS 和组件调整
2. **状态管理**：Zustand 相对简单

## 成功标准

### 功能标准
1. ✅ 项目 CRUD 操作完全正常
2. ✅ 聊天功能与原系统功能一致
3. ✅ React Flow 画板可以展示和编辑节点
4. ✅ Agent 可以通过消息更新画板内容

### 性能标准
1. ✅ 页面加载时间 < 2秒
2. ✅ 聊天响应时间 < 500ms
3. ✅ 画板操作响应时间 < 100ms

### 用户体验标准
1. ✅ UI 设计还原度 > 90%
2. ✅ 响应式设计支持移动端
3. ✅ 无明显 Bug 和崩溃

---

## 开始执行

接下来将按照以上计划开始实施，首先从修复 Project API 问题开始。 