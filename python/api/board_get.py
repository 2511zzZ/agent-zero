from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers import files
import json


class GetBoard(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        ctxid = input.get("context", [])
        context = self.get_context(ctxid)
        
        # 构建board文件路径
        board_file = f"memory/board_{context.id}.json"
        
        try:
            # 尝试读取board文件
            board_data = files.read_file(board_file)
            board_state = json.loads(board_data)
            
            # 计算统计信息
            plan_count = len(board_state.get('plan', []))
            final_artifacts_count = len(board_state.get('final_artifacts', []))
            
            return {
                "board": board_state,
                "plan_count": plan_count,
                "final_artifacts_count": final_artifacts_count,
                "last_updated": board_state.get('last_updated', 0)
            }
            
        except Exception as e:
            # 如果文件不存在或读取失败，返回空的board状态
            return {
                "board": {
                    "plan": [],
                    "final_artifacts": [],
                    "last_updated": 0
                },
                "plan_count": 0,
                "final_artifacts_count": 0,
                "last_updated": 0
            } 