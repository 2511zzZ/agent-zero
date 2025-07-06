# 🧪 Board UI 测试指南

## 📋 实现完成情况

### ✅ 已完成的功能

1. **项目结构**
   - React + TypeScript 项目配置
   - Vite 构建工具配置
   - Ant Design + Tailwind CSS 样式系统

2. **后端增强**
   - 增强的 `BoardOutputEnhancedTool` 工具
   - 新的 `board_update` API 端点
   - 增强的 `board_get` API 端点
   - 兼容旧格式的数据转换

3. **前端组件**
   - React Flow 集成的无限画布
   - 4种节点类型组件 (Plan, Milestone, Deliverable, Note)
   - Chat 面板组件
   - Zustand 状态管理

4. **Docker 集成**
   - Node.js 安装脚本
   - 前端构建脚本
   - 开发服务器启动脚本

5. **测试方案**
   - Board Output 工具测试
   - 可视化测试页面
   - 测试数据生成器
   - 完整测试套件

## 🔧 测试步骤

### 1. 测试 Board Output 工具

```bash
# 设置Python路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 运行board_output工具测试
python tests/test_board_output.py
```

**预期结果**: 8个测试用例全部通过，生成 `memory/board_test_board.json` 文件

### 2. 生成测试数据

```bash
# 生成各种场景的测试数据
python tests/generate_test_data.py
```

**预期结果**: 在 `tests/data/` 目录生成4个JSON文件：
- `board_simple_project.json` - 简单项目
- `board_complex_project.json` - 复杂项目  
- `board_mixed_nodes.json` - 混合节点类型
- `board_stress_test.json` - 压力测试 (50个节点)

### 3. 启动可视化测试

```bash
# 启动HTTP服务器
python3 -m http.server 8000
```

然后访问: http://localhost:8000/tests/board_test.html

**测试内容**:
- 加载不同测试场景
- 查看节点可视化效果
- 测试API连接
- 上传自定义JSON文件
- 实时添加/编辑/删除节点

### 4. 安装前端依赖（可选）

```bash
cd board-ui
npm install
```

### 5. 启动前端开发服务器（可选）

```bash
cd board-ui
npm run dev
```

访问: http://localhost:3001

## 🎯 功能测试点

### Board Output 工具测试
- [ ] 创建初始计划节点
- [ ] 添加产物到节点
- [ ] 创建节点连接关系
- [ ] 更新节点状态
- [ ] 增量更新功能
- [ ] 创建不同类型节点
- [ ] 更新视图状态
- [ ] 删除节点功能

### 可视化测试
- [ ] 简单项目场景加载
- [ ] 复杂项目场景加载
- [ ] 混合节点场景加载
- [ ] 压力测试场景加载
- [ ] JSON文件上传功能
- [ ] 数据导出功能
- [ ] API连接测试
- [ ] 实时节点操作

### React组件测试（需要前端服务器）
- [ ] Board Canvas 渲染
- [ ] 节点类型显示正确
- [ ] 节点编辑功能
- [ ] 连接创建功能
- [ ] Chat面板功能
- [ ] 响应式布局

## 📊 测试数据说明

### 简单项目 (2个节点)
- 项目启动节点 (已完成)
- 需求分析节点 (进行中)
- 包含文档和原型产物

### 复杂项目 (20个节点)
- 5个阶段里程碑
- 15个具体任务
- 多层级连接关系

### 混合节点 (4个节点)
- Plan节点: 市场调研
- Milestone节点: MVP发布
- Deliverable节点: API文档
- Note节点: 技术决策

### 压力测试 (50个节点)
- 随机分布的节点类型
- 随机连接关系
- 测试性能和渲染

## 🚨 已知限制

1. **前端服务器**: 需要安装Node.js和npm依赖
2. **API集成**: 需要后端服务器运行
3. **Docker构建**: 需要Docker环境
4. **文件权限**: 某些脚本可能需要执行权限

## 🔍 调试提示

### 检查生成的数据
```bash
# 查看board状态文件
cat memory/board_test_board.json | python -m json.tool

# 查看测试数据
ls -la tests/data/
```

### 查看API响应
```javascript
// 在浏览器控制台测试API
fetch('/api/board_get', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ context: 'test' })
}).then(r => r.json()).then(console.log);
```

### 前端开发调试
```bash
# 查看前端构建输出
cd board-ui && npm run build
ls -la ../webui/board/
```

## 📝 测试报告格式

请按以下格式报告测试结果：

```
✅ PASS - 功能正常
❌ FAIL - 功能异常，错误信息: xxx
⚠️  WARN - 部分功能正常，但有问题: xxx
🔧 SKIP - 跳过测试，原因: xxx
```

## 🎉 下一步

测试完成后，可以考虑：
1. 集成到主应用中
2. 添加更多节点类型
3. 实现协作功能
4. 优化性能
5. 添加更多测试用例


curl 'http://localhost:50080/message_async' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b '__next_hmr_refresh_hash__=18; session=eyJjc3JmX3Rva2VuIjoiN1FFQXktdTFDNDlibnJaUmZvMXRNazkwX0R0TlJkT25DWm84TzZPNVBsTSJ9.aGqK1Q.3iTLMyRR5Ufn8Cgxiox0rd1hofA' \
  -H 'DNT: 1' \
  -H 'Origin: http://localhost:50080' \
  -H 'Referer: http://localhost:50080/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'X-CSRF-Token: 7QEAy-u1C49bnrZRfo1tMk90_DtNRdOnCZo8O6O5PlM' \
  --data-raw '{"text":"test","context":"eba24e92-4ab8-42f4-b683-cceb2da09309","message_id":"deb2f291-7b92-487a-ab54-d312b251d965"}'


  curl 'http://localhost:50301/poll' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b '__next_hmr_refresh_hash__=18; session=eyJjc3JmX3Rva2VuIjoiN1FFQXktdTFDNDlibnJaUmZvMXRNazkwX0R0TlJkT25DWm84TzZPNVBsTSJ9.aGqK1Q.3iTLMyRR5Ufn8Cgxiox0rd1hofA' \
  -H 'DNT: 1' \
  -H 'Origin: http://localhost:50301' \
  -H 'Referer: http://localhost:50301/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw '{"log_from":0,"context":"default","timezone":"Asia/Shanghai"}'