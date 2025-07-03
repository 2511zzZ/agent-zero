from dataclasses import dataclass
from typing import List, Dict, Any
from python.helpers.tool import Tool, Response
import time
from python.helpers import files
from python.tools.board_output import BoardItem

# 画板编辑操作
@dataclass
class BoardEdit:
    action: str  # add, update, delete
    item: BoardItem

# 画板编辑请求
@dataclass
class BoardEditRequest:
    edits: List[BoardEdit]
    user_id: str
    timestamp: float

class BoardInputTool(Tool):
    async def execute(self, edits: List[dict] | None = None, user_id: str = '', **kwargs):
        # 读取当前 board 状态
        board_file = f"memory/board_{self.agent.agent_name}.json"
        try:
            board_data = files.read_file(board_file)
            board_state = files.json.loads(board_data)
            items = [BoardItem(**item) for item in board_state.get("items", [])]
        except Exception:
            items = []
        # 应用编辑操作
        if edits is None:
            edits = []
        for edit in edits:
            action = edit.get("action")
            item = BoardItem(**edit["item"])
            if action == "add":
                items.append(item)
            elif action == "update":
                items = [item if i.id == item.id else i for i in items]
            elif action == "delete":
                items = [i for i in items if i.id != item.id]
        # 更新 board 状态
        new_state = {"items": [i.__dict__ for i in items], "last_updated": time.time()}
        files.write_file(board_file, files.json.dumps(new_state, ensure_ascii=False))
        return Response(message=f"Board updated by user {user_id}.", break_loop=False) 