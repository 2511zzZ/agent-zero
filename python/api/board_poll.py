from python.helpers.api import ApiHandler
from python.helpers import files
from flask import Request, Response
import json
import time
from typing import Optional


class BoardPoll(ApiHandler):
    """Board轮询API端点，用于获取board数据的实时更新"""
    
    async def process(self, input: dict, request: Request) -> dict | Response:
        try:
            # 获取参数
            context_id = input.get('context') or input.get('ctxid', 'default')
            last_version = input.get('last_version', 0)
            
            # 构建board文件路径
            board_file = f"memory/board_{context_id}.json"
            
            # 默认返回数据
            response_data = {
                'version': last_version,
                'has_updates': False,
                'board_data': None,
                'timestamp': None
            }
            
            try:
                # 尝试读取board文件
                if files.exists(board_file):
                    board_content = files.read_file(board_file)
                    board_data = json.loads(board_content)
                    
                    # 只支持新格式
                    if 'version' not in board_data:
                        print(f"[BoardPoll] Ignoring legacy format board for context {context_id}")
                        board_data = None
                    
                    current_version = board_data.get('version', 0) if board_data else 0
                    
                    # 检查是否有更新
                    if board_data and current_version > last_version:
                        response_data.update({
                            'version': current_version,
                            'has_updates': True,
                            'board_data': board_data,
                            'timestamp': board_data.get('metadata', {}).get('updated_at')
                        })
                        print(f"[BoardPoll] Board updated: version {current_version} for context {context_id}")
                    elif board_data:
                        response_data['version'] = current_version
                        print(f"[BoardPoll] No updates: version {current_version} for context {context_id}")
                    else:
                        print(f"[BoardPoll] No valid board data for context {context_id}")
                else:
                    # 文件不存在，返回空的board数据
                    print(f"[BoardPoll] No board file found for context {context_id}")
                    response_data.update({
                        'version': 0,
                        'has_updates': False,
                        'board_data': {
                            'version': 0,
                            'nodes': {},
                            'connections': {},
                            'viewport': {'x': 0, 'y': 0, 'scale': 1},
                            'layout': {'grid_size': 20, 'snap_to_grid': True},
                            'metadata': {
                                'title': 'New Board',
                                'description': '',
                                'tags': []
                            }
                        }
                    })
                    
            except Exception as e:
                print(f"[BoardPoll] Error reading board file: {e}")
                # 返回空的board数据
                response_data.update({
                    'version': 0,
                    'has_updates': False,
                    'board_data': {
                        'version': 0,
                        'nodes': {},
                        'connections': {},
                        'viewport': {'x': 0, 'y': 0, 'scale': 1},
                        'layout': {'grid_size': 20, 'snap_to_grid': True},
                        'metadata': {
                            'title': 'New Board',
                            'description': '',
                            'tags': []
                        }
                    }
                })
            
            return response_data
            
        except Exception as e:
            print(f"[BoardPoll] Unexpected error: {e}")
            return {
                'version': 0,
                'has_updates': False,
                'board_data': None,
                'error': str(e)
            }
    
