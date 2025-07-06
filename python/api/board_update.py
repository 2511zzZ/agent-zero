from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers import files
import json
import time
import uuid


class UpdateBoard(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        try:
            context_id = input.get("context", "default")
            operation = input.get("operation", "update")
            nodes = input.get("nodes", [])
            connections = input.get("connections", [])
            viewport = input.get("viewport")
            metadata = input.get("metadata")
            
            print(f"[BoardUpdate] Operation: {operation}, Context: {context_id}")
            
            # 加载现有board状态
            board_file = f"memory/board_{context_id}.json"
            try:
                board_data = files.read_file(board_file)
                board_state = json.loads(board_data)
            except Exception as e:
                print(f"[BoardUpdate] Creating new board: {e}")
                board_state = {
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
                        "last_editor": "user"
                    }
                }
            
            # 执行操作
            if operation == "update" or operation == "create":
                self._update_nodes(board_state, nodes)
            elif operation == "delete":
                self._delete_nodes(board_state, nodes)
            elif operation == "connect":
                self._update_connections(board_state, connections)
            
            # 更新连接
            if connections and operation != "delete":
                self._update_connections(board_state, connections)
            
            # 更新视图状态
            if viewport:
                board_state["viewport"].update(viewport)
            
            # 更新元数据
            if metadata:
                board_state["metadata"].update(metadata)
            
            # 更新版本和时间戳
            board_state["version"] += 1
            board_state["metadata"]["updated_at"] = time.time()
            
            # 保存状态
            files.write_file(board_file, json.dumps(board_state, ensure_ascii=False, indent=2))
            
            # 计算统计信息
            node_count = len(board_state["nodes"])
            connection_count = len(board_state["connections"])
            
            return {
                "success": True,
                "message": f"Board {operation} completed",
                "board": board_state,
                "stats": {
                    "node_count": node_count,
                    "connection_count": connection_count,
                    "last_updated": board_state["metadata"]["updated_at"]
                }
            }
            
        except Exception as e:
            print(f"[BoardUpdate] Error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update board"
            }
    
    def _update_nodes(self, board_state: dict, nodes: list):
        """更新节点"""
        for node_data in nodes:
            node_id = node_data.get("id")
            if not node_id:
                node_id = str(uuid.uuid4())
                node_data["id"] = node_id
            
            current_time = time.time()
            
            if node_id in board_state["nodes"]:
                # 更新现有节点
                existing_node = board_state["nodes"][node_id]
                for key, value in node_data.items():
                    if key == "content" and isinstance(value, dict):
                        # 合并content字段
                        if "content" not in existing_node:
                            existing_node["content"] = {}
                        existing_node["content"].update(value)
                    else:
                        existing_node[key] = value
                existing_node["updated_at"] = current_time
                print(f"[BoardUpdate] Updated node {node_id}")
            else:
                # 创建新节点
                node_data.setdefault("created_at", current_time)
                node_data.setdefault("updated_at", current_time)
                node_data.setdefault("type", "plan")
                node_data.setdefault("status", "pending")
                node_data.setdefault("priority", "medium")
                node_data.setdefault("position", {"x": 100, "y": 100})
                node_data.setdefault("size", {"width": 200, "height": 150})
                node_data.setdefault("color", "#3B82F6")
                node_data.setdefault("content", {"artifacts": [], "tags": [], "metadata": {}})
                node_data.setdefault("children_ids", [])
                node_data.setdefault("dependencies", [])
                
                board_state["nodes"][node_id] = node_data
                print(f"[BoardUpdate] Created node {node_id}")
    
    def _delete_nodes(self, board_state: dict, nodes: list):
        """删除节点"""
        for node_data in nodes:
            node_id = node_data.get("id")
            if node_id and node_id in board_state["nodes"]:
                del board_state["nodes"][node_id]
                print(f"[BoardUpdate] Deleted node {node_id}")
                
                # 删除相关连接
                to_delete = []
                for conn_id, conn in board_state["connections"].items():
                    if conn.get("source_id") == node_id or conn.get("target_id") == node_id:
                        to_delete.append(conn_id)
                
                for conn_id in to_delete:
                    del board_state["connections"][conn_id]
                    print(f"[BoardUpdate] Deleted connection {conn_id}")
    
    def _update_connections(self, board_state: dict, connections: list):
        """更新连接"""
        for conn_data in connections:
            conn_id = conn_data.get("id", str(uuid.uuid4()))
            conn_data["id"] = conn_id
            
            conn_data.setdefault("type", "dependency")
            conn_data.setdefault("label", "")
            conn_data.setdefault("style", {"color": "#666666", "width": 2})
            
            board_state["connections"][conn_id] = conn_data
            print(f"[BoardUpdate] Updated connection {conn_id}")