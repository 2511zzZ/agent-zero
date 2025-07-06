from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from python.helpers.tool import Tool, Response
import time
import json
from python.helpers import files
import uuid


@dataclass
class EnhancedBoardNode:
    id: str
    type: str = 'plan'  # 'plan' | 'milestone' | 'deliverable' | 'note'
    name: str = ''
    description: str = ''
    status: str = 'pending'  # 'pending' | 'in_progress' | 'completed' | 'blocked'
    priority: str = 'medium'  # 'low' | 'medium' | 'high' | 'critical'
    
    # 可视化属性
    position: Dict[str, float] = field(default_factory=lambda: {'x': 0, 'y': 0})
    size: Dict[str, float] = field(default_factory=lambda: {'width': 200, 'height': 150})
    color: str = '#3B82F6'
    
    # 内容属性
    content: Dict[str, Any] = field(default_factory=lambda: {
        'text': '',
        'artifacts': [],
        'links': [],
        'tags': [],
        'metadata': {}
    })
    
    # 关系属性
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    # 时间属性
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    due_date: Optional[float] = None
    completed_at: Optional[float] = None


@dataclass
class BoardConnection:
    id: str
    source_id: str
    target_id: str
    type: str = 'dependency'  # 'dependency' | 'parent_child' | 'reference' | 'flow'
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
    
    # 视图状态
    viewport: Dict[str, float] = field(default_factory=lambda: {
        'x': 0,
        'y': 0,
        'scale': 1
    })
    
    # 布局设置
    layout: Dict[str, Any] = field(default_factory=lambda: {
        'grid_size': 20,
        'snap_to_grid': True,
        'auto_layout': False
    })
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=lambda: {
        'title': 'New Board',
        'description': '',
        'tags': [],
        'created_at': time.time(),
        'updated_at': time.time(),
        'last_editor': 'system'
    })


class BoardOutputEnhancedTool(Tool):
    
    def _load_board_state(self, context_id: str) -> EnhancedBoardState:
        """加载board状态"""
        board_file = f"memory/board_{context_id}.json"
        try:
            board_data = files.read_file(board_file)
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
            
            print(f"[BoardOutputEnhanced] Loaded board with {len(board_state.nodes)} nodes, {len(board_state.connections)} connections")
            return board_state
            
        except Exception as e:
            print(f"[BoardOutputEnhanced] Failed to load board state: {e}")
            return EnhancedBoardState()
    
    def _save_board_state(self, board_state: EnhancedBoardState, context_id: str):
        """保存board状态"""
        board_file = f"memory/board_{context_id}.json"
        
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
        
        files.write_file(board_file, json.dumps(board_dict, ensure_ascii=False, indent=2))
        print(f"[BoardOutputEnhanced] Saved board state to {board_file}")
    
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
                print(f"[BoardOutputEnhanced] Updated node {node_id}")
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
                print(f"[BoardOutputEnhanced] Created node {node_id}")
    
    def _create_connections(self, board_state: EnhancedBoardState, connections: List[dict]):
        """创建连接"""
        for conn_data in connections:
            conn_id = conn_data.get('id', str(uuid.uuid4()))
            conn_data['id'] = conn_id
            
            conn_data.setdefault('type', 'dependency')
            conn_data.setdefault('label', '')
            conn_data.setdefault('style', {'color': '#666666', 'width': 2})
            
            board_state.connections[conn_id] = BoardConnection(**conn_data)
            print(f"[BoardOutputEnhanced] Created connection {conn_id}")
    
    def _delete_nodes(self, board_state: EnhancedBoardState, node_ids: List[str]):
        """删除节点"""
        for node_id in node_ids:
            if node_id in board_state.nodes:
                del board_state.nodes[node_id]
                print(f"[BoardOutputEnhanced] Deleted node {node_id}")
                
                # 删除相关连接
                to_delete = []
                for conn_id, conn in board_state.connections.items():
                    if conn.source_id == node_id or conn.target_id == node_id:
                        to_delete.append(conn_id)
                
                for conn_id in to_delete:
                    del board_state.connections[conn_id]
                    print(f"[BoardOutputEnhanced] Deleted connection {conn_id}")
    
    async def execute(self, 
                     operation: str = 'update',  # update, create, delete, move, connect
                     nodes: Optional[List[dict]] = None,
                     connections: Optional[List[dict]] = None,
                     viewport: Optional[dict] = None,
                     metadata: Optional[dict] = None,
                     chat_id: Optional[str] = None,
                     **kwargs):
        
        print(f"[BoardOutputEnhanced] Operation: {operation}")
        
        # 获取上下文ID
        context_id = chat_id or getattr(self.agent.context, 'id', None) or 'default'
        
        # 加载当前状态
        board_state = self._load_board_state(context_id)
        
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
        self._save_board_state(board_state, context_id)
        
        node_count = len(board_state.nodes)
        conn_count = len(board_state.connections)
        
        return Response(
            message=f"Board {operation} completed. Nodes: {node_count}, Connections: {conn_count}",
            break_loop=False
        )