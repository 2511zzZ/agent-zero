from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers import files
from python.api.project_common import ProjectCommon
import json
import time
import uuid

from python.helpers.print_style import PrintStyle


class ProjectCreate(ApiHandler):
    
    @classmethod
    def get_methods(cls) -> list[str]:
        return ["POST"]
    
    async def process(self, input: dict, request: Request) -> dict | Response:
        try:
            # 验证必要字段
            if 'name' not in input or not input['name'].strip():
                return {
                    "success": False,
                    "error": "Project name is required"
                }
            
            # 创建项目数据
            project_id = str(uuid.uuid4())
            now = time.time()
            
            project = {
                'id': project_id,
                'name': input['name'].strip(),
                'description': input.get('description', '').strip(),
                'status': input.get('status', 'active'),
                'createdAt': now,
                'updatedAt': now,
                'flowchart': {
                    'nodes': [],
                    'edges': [],
                    'viewport': {'x': 0, 'y': 0, 'zoom': 1},
                    'version': 0
                },
                'chatHistory': []
            }
            
            # 确保项目目录存在并保存文件
            ProjectCommon.ensure_projects_dir()
            project_file = ProjectCommon.get_project_file_path(project_id)
            files.write_file(project_file, json.dumps(project, indent=2))
            
            return {
                "success": True,
                "project": project
            }
            
        except Exception as e:
            PrintStyle().standard(f"[ProjectCreate] Error: {e}")
            return {
                "success": False,
                "error": str(e)
            }