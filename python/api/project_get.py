from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers import files
from python.api.project_common import ProjectCommon
import json
import os

from python.helpers.print_style import PrintStyle


class ProjectGet(ApiHandler):
    
    @classmethod
    def get_methods(cls) -> list[str]:
        return ["POST"]
    
    async def process(self, input: dict, request: Request) -> dict | Response:
        try:
            # 验证项目 ID
            project_id = input.get('project_id')
            if not project_id:
                return {
                    "success": False,
                    "error": "Project ID is required"
                }
            
            # 获取项目文件路径
            project_file = ProjectCommon.get_project_file_path(project_id)
            
            if not os.path.exists(project_file):
                return {
                    "success": False,
                    "error": "Project not found"
                }
            
            # 读取并规范化项目数据
            project_data = files.read_file(project_file)
            project = json.loads(project_data)
            project = ProjectCommon.normalize_project(project)
            
            return {
                "success": True,
                "project": project
            }
            
        except json.JSONDecodeError as e:
            project_id = input.get('project_id', 'unknown')
            PrintStyle().standard(f"[ProjectGet] Invalid JSON for project {project_id}: {e}")
            return {
                "success": False,
                "error": "Invalid project data format"
            }
        except Exception as e:
            PrintStyle().standard(f"[ProjectGet] Error: {e}")
            return {
                "success": False,
                "error": str(e)
            }