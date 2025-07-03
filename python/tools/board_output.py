from dataclasses import dataclass, field
from typing import List, Dict, Any
from python.helpers.tool import Tool, Response
import time
from python.helpers import files

# 画板上的单个元素（如计划、产物、备注等）
@dataclass
class BoardItem:
    id: str
    type: str  # 例如 plan, artifact, note
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

# 画板整体状态
@dataclass
class BoardState:
    items: List[BoardItem]
    last_updated: float

class BoardOutputTool(Tool):
    async def execute(self, items: List[dict] | None = None, **kwargs):
        # items 为结构化的 BoardItem 字典列表
        if items is None:
            items = []
        # 读取已有 board 状态
        board_file = f"memory/board_{self.agent.agent_name}.json"
        try:
            board_data = files.read_file(board_file)
            board_state = files.json.loads(board_data)
            existing_items = {item['id']: BoardItem(**item) for item in board_state.get('items', [])}
        except Exception:
            existing_items = {}
        # 合并新 items，id 相同则覆盖，否则追加
        for item in items:
            board_item = BoardItem(**item)
            existing_items[board_item.id] = board_item
        merged_items = list(existing_items.values())
        board_state = BoardState(items=merged_items, last_updated=time.time())
        # 持久化到文件
        files.write_file(board_file, files.json.dumps(board_state, default=lambda o: o.__dict__, ensure_ascii=False))
        # 返回当前 board 状态
        return Response(message=f"Board updated with {len(merged_items)} items.", break_loop=False) 