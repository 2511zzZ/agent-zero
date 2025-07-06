from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from python.helpers.tool import Tool, Response
import time
from python.helpers import files
import json
import uuid

class BoardOutputTool(Tool):
    
    def _load_board_state(self, context_id: str) -> dict:
        """加载board状态，使用新格式"""
        board_file = f"memory/board_{context_id}.json"
        try:
            board_data = files.read_file(board_file)
            board_state = json.loads(board_data)
            
            # 检查是否为旧格式并转换
            if 'plan' in board_state and 'version' not in board_state:
                print(f"[BoardOutputTool] Converting legacy format for context {context_id}")
                board_state = self._convert_legacy_format(board_state)
            
            # 确保是新格式
            if 'version' not in board_state:
                board_state = self._create_empty_board()
            
            return board_state
            
        except Exception as e:
            print(f"[BoardOutputTool] Failed to load board state: {e}")
            return self._create_empty_board()
    
    def _create_empty_board(self) -> dict:
        """创建空的新格式board"""
        return {
            'version': 1,
            'nodes': {},
            'connections': {},
            'viewport': {'x': 0, 'y': 0, 'scale': 1},
            'layout': {'grid_size': 20, 'snap_to_grid': True, 'auto_layout': False},
            'metadata': {
                'title': 'New Board',
                'description': '',
                'tags': [],
                'created_at': time.time(),
                'updated_at': time.time(),
                'last_editor': 'board_output'
            }
        }
    
    def _convert_legacy_format(self, legacy_board: dict) -> dict:
        """转换旧格式到新格式"""
        board_state = self._create_empty_board()
        
        # 转换plan节点
        plan_nodes = legacy_board.get('plan', [])
        for i, node in enumerate(plan_nodes):
            if isinstance(node, dict) and 'id' in node:
                node_id = node['id']
                board_state['nodes'][node_id] = {
                    'id': node_id,
                    'type': 'plan',
                    'name': node.get('name', ''),
                    'description': node.get('description', ''),
                    'status': 'pending',
                    'priority': 'medium',
                    'position': {'x': 100 + (i % 3) * 250, 'y': 100 + (i // 3) * 200},
                    'size': {'width': 200, 'height': 150},
                    'color': '#3B82F6',
                    'content': {
                        'text': node.get('description', ''),
                        'artifacts': node.get('artifacts', []),
                        'tags': [],
                        'metadata': {}
                    },
                    'parent_id': None,
                    'children_ids': [],
                    'dependencies': [],
                    'created_at': time.time(),
                    'updated_at': time.time()
                }
        
        return board_state
    
    def _save_board_state(self, board_state: dict, context_id: str):
        """保存board状态"""
        board_file = f"memory/board_{context_id}.json"
        board_state['version'] += 1
        board_state['metadata']['updated_at'] = time.time()
        
        files.write_file(board_file, json.dumps(board_state, ensure_ascii=False, indent=2))
        print(f"[BoardOutputTool] Saved board state to {board_file}")
    
    async def execute(self, plan: Optional[List[dict]] = None, final_artifacts: Optional[List[dict]] = None, chat_id: Optional[str] = None, **kwargs):
        print(f"[BoardOutputTool] Called with plan={plan}, final_artifacts={final_artifacts}")
        
        # 获取上下文ID
        context_id = chat_id or getattr(self.agent.context, 'id', None) or 'default'
        
        # 加载当前状态
        board_state = self._load_board_state(context_id)
        
        # 转换并合并plan节点
        if plan:
            for i, node_dict in enumerate(plan):
                node_id = node_dict.get('id')
                if not node_id:
                    node_id = str(uuid.uuid4())
                    node_dict['id'] = node_id
                
                current_time = time.time()
                
                if node_id in board_state['nodes']:
                    # 更新现有节点
                    node = board_state['nodes'][node_id]
                    node['name'] = node_dict.get('name', node['name'])
                    node['description'] = node_dict.get('description', node['description'])
                    
                    # 合并artifacts
                    if 'artifacts' in node_dict:
                        node['content']['artifacts'] = node_dict['artifacts']
                    
                    node['updated_at'] = current_time
                    print(f"[BoardOutputTool] Updated node {node_id}")
                else:
                    # 创建新节点
                    board_state['nodes'][node_id] = {
                        'id': node_id,
                        'type': 'plan',
                        'name': node_dict.get('name', ''),
                        'description': node_dict.get('description', ''),
                        'status': 'pending',
                        'priority': 'medium',
                        'position': {'x': 100 + (i % 3) * 250, 'y': 100 + (i // 3) * 200},
                        'size': {'width': 200, 'height': 150},
                        'color': '#3B82F6',
                        'content': {
                            'text': node_dict.get('description', ''),
                            'artifacts': node_dict.get('artifacts', []),
                            'tags': [],
                            'metadata': {}
                        },
                        'parent_id': None,
                        'children_ids': [],
                        'dependencies': [],
                        'created_at': current_time,
                        'updated_at': current_time
                    }
                    print(f"[BoardOutputTool] Created node {node_id}")
        
        # 处理final_artifacts（添加到metadata中）
        if final_artifacts:
            board_state['metadata']['final_artifacts'] = final_artifacts
            print(f"[BoardOutputTool] Updated final_artifacts: {final_artifacts}")
        
        # 保存状态
        self._save_board_state(board_state, context_id)
        
        node_count = len(board_state['nodes'])
        
        return Response(
            message=f"Board updated. Nodes: {node_count}, Version: {board_state['version']}",
            break_loop=False
        ) 