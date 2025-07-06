from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers import files
import json
import time


class GetBoard(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        context_id = input.get("context", "default")
        
        # 如果传入的是context对象，获取其id
        if hasattr(context_id, 'id'):
            context_id = context_id.id
        elif isinstance(context_id, list) and len(context_id) > 0:
            context_id = context_id[0]
        
        # 构建board文件路径
        board_file = f"memory/board_{context_id}.json"
        
        try:
            # 尝试读取board文件
            board_data = files.read_file(board_file)
            board_state = json.loads(board_data)
            
            # 确保board状态包含所有必需字段
            if "nodes" not in board_state:
                # 兼容旧格式
                board_state = self._convert_legacy_format(board_state)
            
            # 计算统计信息
            node_count = len(board_state.get('nodes', {}))
            connection_count = len(board_state.get('connections', {}))
            
            return {
                "success": True,
                "board": board_state,
                "stats": {
                    "node_count": node_count,
                    "connection_count": connection_count,
                    "last_updated": board_state.get('metadata', {}).get('updated_at', 0)
                }
            }
            
        except Exception as e:
            print(f"[GetBoard] Error loading board {context_id}: {e}")
            # 如果文件不存在或读取失败，返回空的board状态
            empty_board = {
                "version": 1,
                "nodes": {},
                "connections": {},
                "viewport": {"x": 0, "y": 0, "scale": 1},
                "layout": {"grid_size": 20, "snap_to_grid": True, "auto_layout": False},
                "metadata": {
                    "title": "New Board",
                    "description": "",
                    "tags": [],
                    "created_at": time.time(),
                    "updated_at": time.time(),
                    "last_editor": "system"
                }
            }
            
            return {
                "success": True,
                "board": empty_board,
                "stats": {
                    "node_count": 0,
                    "connection_count": 0,
                    "last_updated": empty_board["metadata"]["updated_at"]
                }
            }
    
    def _convert_legacy_format(self, legacy_board: dict) -> dict:
        """转换旧格式的board数据到新格式"""
        nodes = {}
        connections = {}
        
        # 转换旧的plan节点
        plan_nodes = legacy_board.get('plan', [])
        for i, node in enumerate(plan_nodes):
            if isinstance(node, dict) and 'id' in node:
                node_id = node['id']
                nodes[node_id] = {
                    "id": node_id,
                    "type": "plan",
                    "name": node.get('name', ''),
                    "description": node.get('description', ''),
                    "status": "pending",
                    "priority": "medium",
                    "position": {"x": 100 + (i % 3) * 250, "y": 100 + (i // 3) * 200},
                    "size": {"width": 200, "height": 150},
                    "color": "#3B82F6",
                    "content": {
                        "artifacts": node.get('artifacts', []),
                        "tags": [],
                        "metadata": {}
                    },
                    "children_ids": [],
                    "dependencies": [],
                    "created_at": time.time(),
                    "updated_at": time.time()
                }
        
        return {
            "version": 1,
            "nodes": nodes,
            "connections": connections,
            "viewport": {"x": 0, "y": 0, "scale": 1},
            "layout": {"grid_size": 20, "snap_to_grid": True, "auto_layout": False},
            "metadata": {
                "title": "Converted Board",
                "description": "Converted from legacy format",
                "tags": [],
                "created_at": legacy_board.get('last_updated', time.time()),
                "updated_at": time.time(),
                "last_editor": "system"
            }
        } 