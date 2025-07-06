from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from python.helpers.tool import Tool, Response
import time
from python.helpers import files
import os

# 计划中的单个节点
@dataclass
class PlanNode:
    id: str
    name: str
    description: str
    artifacts: List[Dict[str, Any]] = field(default_factory=list)  # 每个产物可包含 file/link

# 画板整体状态
@dataclass
class BoardState:
    plan: List[PlanNode] = field(default_factory=list)  # 计划的节点列表
    final_artifacts: List[Dict[str, Any]] = field(default_factory=list)  # 最终产物
    last_updated: float = 0.0

class BoardOutputTool(Tool):
    async def execute(self, plan: Optional[List[dict]] = None, final_artifacts: Optional[List[dict]] = None, chat_id: Optional[str] = None, **kwargs):
        print(f"[BoardOutputTool] Called with plan={plan}, final_artifacts={final_artifacts}")
        # 优先使用传入 chat_id，否则用 agent.context.id
        cid = chat_id or getattr(self.agent.context, 'id', None) or 'default'
        board_file = f"memory/board_{cid}.json"
        # 读取已有 board 状态
        try:
            board_data = files.read_file(board_file)
            board_state_dict = files.json.loads(board_data)
            print(f"[BoardOutputTool] Loaded existing board state: {board_state_dict}")
            plan_nodes = [PlanNode(**node) for node in board_state_dict.get('plan', [])]
            final_artifacts_list = board_state_dict.get('final_artifacts', [])
        except Exception as e:
            print(f"[BoardOutputTool] No existing board or failed to load: {e}")
            plan_nodes = []
            final_artifacts_list = []
        # 增量合并 plan
        if plan:
            plan_map = {node.id: node for node in plan_nodes}
            for node_dict in plan:
                node_id = node_dict.get('id')
                if not node_id:
                    continue
                if node_id in plan_map:
                    node = plan_map[node_id]
                    node.name = node_dict.get('name', node.name)
                    node.description = node_dict.get('description', node.description)
                    old_files = {a.get('file'): a for a in node.artifacts if 'file' in a}
                    for art in node_dict.get('artifacts', []):
                        fkey = art.get('file')
                        if fkey and fkey not in old_files:
                            node.artifacts.append(art)
                    for art in node_dict.get('artifacts', []):
                        fkey = art.get('file')
                        if fkey:
                            old_files[fkey] = art
                    node.artifacts = list(old_files.values())
                    print(f"[BoardOutputTool] Updated node {node_id}: {node}")
                else:
                    plan_map[node_id] = PlanNode(**node_dict)
                    print(f"[BoardOutputTool] Added new node {node_id}: {node_dict}")
            plan_nodes = list(plan_map.values())
        # 增量合并 final_artifacts（以 file 字段去重）
        if final_artifacts:
            file_map = {a.get('file'): a for a in final_artifacts_list if 'file' in a}
            for art in final_artifacts:
                fkey = art.get('file')
                if fkey:
                    file_map[fkey] = art
            final_artifacts_list = list(file_map.values())
            print(f"[BoardOutputTool] Updated final_artifacts: {final_artifacts_list}")
        board_state = BoardState(plan=plan_nodes, final_artifacts=final_artifacts_list, last_updated=time.time())
        files.write_file(board_file, files.json.dumps(board_state, default=lambda o: o.__dict__, ensure_ascii=False))
        print(f"[BoardOutputTool] Board state saved. Plan nodes: {len(plan_nodes)}, Final artifacts: {len(final_artifacts_list)}")
        return Response(message=f"Board updated. Plan nodes: {len(plan_nodes)}, Final artifacts: {len(final_artifacts_list)}", break_loop=False) 