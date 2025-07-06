#!/usr/bin/env python3
"""
简化版Board Output工具测试
不依赖完整的Agent Zero环境
"""

import sys
import os
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 简化的工具基类
class MockResponse:
    def __init__(self, message, break_loop=False):
        self.message = message
        self.break_loop = break_loop

class MockTool:
    def __init__(self):
        self.agent = None

# 简化的文件操作
class MockFiles:
    @staticmethod
    def read_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_file(filepath, content):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

# 复制增强的数据结构
@dataclass
class EnhancedBoardNode:
    id: str
    type: str = 'plan'
    name: str = ''
    description: str = ''
    status: str = 'pending'
    priority: str = 'medium'
    position: Dict[str, float] = field(default_factory=lambda: {'x': 0, 'y': 0})
    size: Dict[str, float] = field(default_factory=lambda: {'width': 200, 'height': 150})
    color: str = '#3B82F6'
    content: Dict[str, Any] = field(default_factory=lambda: {
        'text': '',
        'artifacts': [],
        'links': [],
        'tags': [],
        'metadata': {}
    })
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    due_date: Optional[float] = None
    completed_at: Optional[float] = None

@dataclass
class BoardConnection:
    id: str
    source_id: str
    target_id: str
    type: str = 'dependency'
    label: str = ''
    style: Dict[str, Any] = field(default_factory=lambda: {
        'color': '#666666',
        'width': 2,
        'dash': []
    })

@dataclass
class EnhancedBoardState:
    version: int = 1
    nodes: Dict[str, EnhancedBoardNode] = field(default_factory=dict)
    connections: Dict[str, BoardConnection] = field(default_factory=dict)
    viewport: Dict[str, float] = field(default_factory=lambda: {'x': 0, 'y': 0, 'scale': 1})
    layout: Dict[str, Any] = field(default_factory=lambda: {
        'grid_size': 20,
        'snap_to_grid': True,
        'auto_layout': False
    })
    metadata: Dict[str, Any] = field(default_factory=lambda: {
        'title': 'New Board',
        'description': '',
        'tags': [],
        'created_at': time.time(),
        'updated_at': time.time(),
        'last_editor': 'system'
    })

class SimpleBoardOutputTool(MockTool):
    """简化版的Board Output工具"""
    
    def __init__(self, context_id="test_board"):
        super().__init__()
        self.context_id = context_id
        self.files = MockFiles()
    
    def _load_board_state(self) -> EnhancedBoardState:
        """加载board状态"""
        board_file = f"memory/board_{self.context_id}.json"
        try:
            board_data = self.files.read_file(board_file)
            board_dict = json.loads(board_data)
            
            # 转换为增强的数据结构
            board_state = EnhancedBoardState()
            board_state.version = board_dict.get('version', 1)
            board_state.viewport = board_dict.get('viewport', board_state.viewport)
            board_state.layout = board_dict.get('layout', board_state.layout)
            board_state.metadata = board_dict.get('metadata', board_state.metadata)
            
            # 转换节点
            nodes_data = board_dict.get('nodes', {})
            for node_id, node_data in nodes_data.items():
                if isinstance(node_data, dict):
                    # 确保所有必需字段存在
                    node_data.setdefault('id', node_id)
                    node_data.setdefault('type', 'plan')
                    node_data.setdefault('name', '')
                    node_data.setdefault('description', '')
                    node_data.setdefault('status', 'pending')
                    node_data.setdefault('priority', 'medium')
                    node_data.setdefault('position', {'x': 0, 'y': 0})
                    node_data.setdefault('size', {'width': 200, 'height': 150})
                    node_data.setdefault('color', '#3B82F6')
                    node_data.setdefault('content', {'artifacts': [], 'tags': [], 'metadata': {}})
                    node_data.setdefault('children_ids', [])
                    node_data.setdefault('dependencies', [])
                    node_data.setdefault('created_at', time.time())
                    node_data.setdefault('updated_at', time.time())
                    
                    board_state.nodes[node_id] = EnhancedBoardNode(**node_data)
            
            # 转换连接
            connections_data = board_dict.get('connections', {})
            for conn_id, conn_data in connections_data.items():
                if isinstance(conn_data, dict):
                    conn_data.setdefault('id', conn_id)
                    conn_data.setdefault('type', 'dependency')
                    conn_data.setdefault('label', '')
                    conn_data.setdefault('style', {'color': '#666666', 'width': 2})
                    board_state.connections[conn_id] = BoardConnection(**conn_data)
            
            print(f"[SimpleBoardTool] Loaded board with {len(board_state.nodes)} nodes, {len(board_state.connections)} connections")
            return board_state
            
        except Exception as e:
            print(f"[SimpleBoardTool] Failed to load board state: {e}")
            return EnhancedBoardState()
    
    def _save_board_state(self, board_state: EnhancedBoardState):
        """保存board状态"""
        board_file = f"memory/board_{self.context_id}.json"
        
        # 转换为可序列化的字典
        board_dict = {
            'version': board_state.version,
            'nodes': {},
            'connections': {},
            'viewport': board_state.viewport,
            'layout': board_state.layout,
            'metadata': board_state.metadata
        }
        
        # 转换节点
        for node_id, node in board_state.nodes.items():
            board_dict['nodes'][node_id] = {
                'id': node.id,
                'type': node.type,
                'name': node.name,
                'description': node.description,
                'status': node.status,
                'priority': node.priority,
                'position': node.position,
                'size': node.size,
                'color': node.color,
                'content': node.content,
                'parent_id': node.parent_id,
                'children_ids': node.children_ids,
                'dependencies': node.dependencies,
                'created_at': node.created_at,
                'updated_at': node.updated_at,
                'due_date': node.due_date,
                'completed_at': node.completed_at
            }
        
        # 转换连接
        for conn_id, conn in board_state.connections.items():
            board_dict['connections'][conn_id] = {
                'id': conn.id,
                'source_id': conn.source_id,
                'target_id': conn.target_id,
                'type': conn.type,
                'label': conn.label,
                'style': conn.style
            }
        
        self.files.write_file(board_file, json.dumps(board_dict, ensure_ascii=False, indent=2))
        print(f"[SimpleBoardTool] Saved board state to {board_file}")
    
    async def execute(self, operation='update', nodes=None, connections=None, viewport=None, metadata=None, **kwargs):
        """执行board操作"""
        print(f"[SimpleBoardTool] Operation: {operation}")
        
        # 加载当前状态
        board_state = self._load_board_state()
        
        # 执行操作
        if operation == 'update' or operation == 'create':
            if nodes:
                self._update_nodes(board_state, nodes)
        elif operation == 'delete':
            if nodes:
                node_ids = [n.get('id') for n in nodes if n.get('id')]
                self._delete_nodes(board_state, node_ids)
        elif operation == 'connect':
            if connections:
                self._create_connections(board_state, connections)
        
        # 更新连接
        if connections and operation != 'delete':
            self._create_connections(board_state, connections)
        
        # 更新视图状态
        if viewport:
            board_state.viewport.update(viewport)
        
        # 更新元数据
        if metadata:
            board_state.metadata.update(metadata)
        
        # 更新版本和时间戳
        board_state.version += 1
        board_state.metadata['updated_at'] = time.time()
        
        # 保存状态
        self._save_board_state(board_state)
        
        node_count = len(board_state.nodes)
        conn_count = len(board_state.connections)
        
        return MockResponse(f"Board {operation} completed. Nodes: {node_count}, Connections: {conn_count}")
    
    def _update_nodes(self, board_state: EnhancedBoardState, nodes: List[dict]):
        """更新节点"""
        for node_data in nodes:
            node_id = node_data.get('id')
            if not node_id:
                node_id = str(uuid.uuid4())
                node_data['id'] = node_id
            
            current_time = time.time()
            
            if node_id in board_state.nodes:
                # 更新现有节点
                node = board_state.nodes[node_id]
                for key, value in node_data.items():
                    if hasattr(node, key):
                        if key == 'content' and isinstance(value, dict):
                            # 合并content字段
                            node.content.update(value)
                        else:
                            setattr(node, key, value)
                node.updated_at = current_time
                print(f"[SimpleBoardTool] Updated node {node_id}")
            else:
                # 创建新节点
                node_data.setdefault('created_at', current_time)
                node_data.setdefault('updated_at', current_time)
                node_data.setdefault('type', 'plan')
                node_data.setdefault('status', 'pending')
                node_data.setdefault('priority', 'medium')
                node_data.setdefault('position', {'x': 100, 'y': 100})
                node_data.setdefault('size', {'width': 200, 'height': 150})
                node_data.setdefault('color', '#3B82F6')
                node_data.setdefault('content', {'artifacts': [], 'tags': [], 'metadata': {}})
                node_data.setdefault('children_ids', [])
                node_data.setdefault('dependencies', [])
                
                board_state.nodes[node_id] = EnhancedBoardNode(**node_data)
                print(f"[SimpleBoardTool] Created node {node_id}")
    
    def _create_connections(self, board_state: EnhancedBoardState, connections: List[dict]):
        """创建连接"""
        for conn_data in connections:
            conn_id = conn_data.get('id', str(uuid.uuid4()))
            conn_data['id'] = conn_id
            
            conn_data.setdefault('type', 'dependency')
            conn_data.setdefault('label', '')
            conn_data.setdefault('style', {'color': '#666666', 'width': 2})
            
            board_state.connections[conn_id] = BoardConnection(**conn_data)
            print(f"[SimpleBoardTool] Created connection {conn_id}")
    
    def _delete_nodes(self, board_state: EnhancedBoardState, node_ids: List[str]):
        """删除节点"""
        for node_id in node_ids:
            if node_id in board_state.nodes:
                del board_state.nodes[node_id]
                print(f"[SimpleBoardTool] Deleted node {node_id}")
                
                # 删除相关连接
                to_delete = []
                for conn_id, conn in board_state.connections.items():
                    if conn.source_id == node_id or conn.target_id == node_id:
                        to_delete.append(conn_id)
                
                for conn_id in to_delete:
                    del board_state.connections[conn_id]
                    print(f"[SimpleBoardTool] Deleted connection {conn_id}")

# 测试用例类
class BoardOutputTester:
    def __init__(self):
        self.tool = SimpleBoardOutputTool()
        self.test_cases = []
        
    def add_test_case(self, name, description, test_data):
        self.test_cases.append({
            'name': name,
            'description': description,
            'data': test_data
        })
    
    async def run_test(self, test_case):
        print(f"\n🧪 Running test: {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        
        try:
            result = await self.tool.execute(**test_case['data'])
            print(f"   ✅ Success: {result.message}")
            return True
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
    
    async def run_all_tests(self):
        print("🚀 Starting board_output simplified tool tests...")
        print("=" * 60)
        
        results = []
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n[{i}/{len(self.test_cases)}]", end=" ")
            success = await self.run_test(test_case)
            results.append(success)
        
        print(f"\n" + "=" * 60)
        print(f"📊 Test Results: {sum(results)}/{len(results)} passed")
        
        if sum(results) == len(results):
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the output above.")
            
        return results

def create_test_cases():
    """创建测试用例"""
    tester = BoardOutputTester()
    
    # 测试1: 创建初始计划
    tester.add_test_case(
        "create_initial_plan",
        "创建包含3个阶段的初始项目计划",
        {
            "operation": "create",
            "nodes": [
                {
                    "id": "phase-1",
                    "type": "plan",
                    "name": "需求分析",
                    "description": "收集和分析项目需求",
                    "status": "pending",
                    "priority": "high",
                    "position": {"x": 100, "y": 100},
                    "color": "#EF4444",
                    "content": {
                        "artifacts": [],
                        "tags": ["requirements", "analysis"]
                    }
                },
                {
                    "id": "phase-2",
                    "type": "milestone",
                    "name": "系统设计",
                    "description": "设计系统架构和技术方案",
                    "status": "pending",
                    "priority": "high",
                    "position": {"x": 100, "y": 300},
                    "color": "#F59E0B",
                    "content": {
                        "artifacts": [],
                        "tags": ["design", "architecture"]
                    }
                },
                {
                    "id": "phase-3",
                    "type": "deliverable",
                    "name": "开发实现",
                    "description": "编码实现和单元测试",
                    "status": "pending",
                    "priority": "medium",
                    "position": {"x": 100, "y": 500},
                    "color": "#10B981",
                    "content": {
                        "artifacts": [],
                        "tags": ["development", "coding"]
                    }
                }
            ]
        }
    )
    
    # 测试2: 添加产物
    tester.add_test_case(
        "add_artifacts",
        "为第一阶段添加需求文档和原型",
        {
            "operation": "update",
            "nodes": [
                {
                    "id": "phase-1",
                    "content": {
                        "artifacts": [
                            {
                                "id": str(uuid.uuid4()),
                                "type": "document",
                                "name": "需求规格说明书",
                                "description": "详细的功能需求文档",
                                "file_path": "/files/requirements.md",
                                "metadata": {"version": "1.0", "author": "产品经理"},
                                "created_at": time.time(),
                                "updated_at": time.time()
                            },
                            {
                                "id": str(uuid.uuid4()),
                                "type": "link",
                                "name": "交互原型",
                                "description": "Figma设计原型",
                                "url": "https://figma.com/proto/123",
                                "metadata": {"tool": "figma", "version": "v1.0"},
                                "created_at": time.time(),
                                "updated_at": time.time()
                            }
                        ]
                    }
                }
            ]
        }
    )
    
    # 测试3: 创建节点连接
    tester.add_test_case(
        "create_connections",
        "创建阶段间的依赖关系",
        {
            "operation": "connect",
            "connections": [
                {
                    "id": "conn-1",
                    "source_id": "phase-1",
                    "target_id": "phase-2",
                    "type": "dependency",
                    "label": "需求完成后开始设计",
                    "style": {"color": "#3B82F6", "width": 2}
                },
                {
                    "id": "conn-2",
                    "source_id": "phase-2",
                    "target_id": "phase-3",
                    "type": "dependency",
                    "label": "设计完成后开始开发",
                    "style": {"color": "#3B82F6", "width": 2}
                }
            ]
        }
    )
    
    # 测试4: 更新节点状态
    tester.add_test_case(
        "update_status",
        "将第一阶段标记为进行中",
        {
            "operation": "update",
            "nodes": [
                {
                    "id": "phase-1",
                    "status": "in_progress",
                    "color": "#3B82F6",
                    "content": {
                        "metadata": {"started_at": time.time()}
                    }
                }
            ]
        }
    )
    
    # 测试5: 创建便签节点
    tester.add_test_case(
        "create_note_node",
        "创建一个便签节点用于记录想法",
        {
            "operation": "create",
            "nodes": [
                {
                    "id": "note-1",
                    "type": "note",
                    "name": "项目想法",
                    "description": "临时记录和想法",
                    "status": "pending",
                    "priority": "low",
                    "position": {"x": 400, "y": 100},
                    "color": "#FACC15",
                    "content": {
                        "text": "这里是一些关于项目的临时想法和备注。\n\n可以多行文本。",
                        "tags": ["idea", "brainstorm"],
                        "artifacts": []
                    }
                }
            ]
        }
    )
    
    # 测试6: 删除节点
    tester.add_test_case(
        "delete_node",
        "删除便签节点",
        {
            "operation": "delete",
            "nodes": [
                {"id": "note-1"}
            ]
        }
    )
    
    return tester

# 主程序
async def main():
    print("🔧 Agent Zero Board Output Simplified Tool Tests")
    print("=" * 60)
    
    # 创建测试器
    tester = create_test_cases()
    
    # 运行所有测试
    results = await tester.run_all_tests()
    
    # 显示最终board状态
    print(f"\n📋 Final Board State:")
    print("-" * 40)
    try:
        with open("memory/board_test_board.json", 'r', encoding='utf-8') as f:
            board_data = f.read()
        board_state = json.loads(board_data)
        
        # 显示统计信息
        node_count = len(board_state.get('nodes', {}))
        conn_count = len(board_state.get('connections', {}))
        version = board_state.get('version', 0)
        
        print(f"📊 Statistics:")
        print(f"   Nodes: {node_count}")
        print(f"   Connections: {conn_count}")
        print(f"   Version: {version}")
        print(f"   Last Updated: {time.ctime(board_state.get('metadata', {}).get('updated_at', 0))}")
        
        # 显示节点类型分布
        if node_count > 0:
            type_counts = {}
            for node in board_state['nodes'].values():
                node_type = node.get('type', 'unknown')
                type_counts[node_type] = type_counts.get(node_type, 0) + 1
            
            print(f"\n📈 Node Types:")
            for node_type, count in type_counts.items():
                print(f"   {node_type}: {count}")
        
        print(f"\n📄 Complete Board JSON (first 500 chars):")
        print("-" * 40)
        formatted_json = json.dumps(board_state, indent=2, ensure_ascii=False)
        if len(formatted_json) > 500:
            print(formatted_json[:500] + "...")
        else:
            print(formatted_json)
        
    except Exception as e:
        print(f"❌ Cannot read board state: {e}")
    
    print(f"\n🏁 Test execution completed!")
    return results

if __name__ == "__main__":
    import asyncio
    results = asyncio.run(main())
    exit_code = 0 if all(results) else 1
    sys.exit(exit_code)