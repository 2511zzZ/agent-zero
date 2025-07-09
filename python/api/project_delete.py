from python.helpers.api import ApiHandler
from flask import Request, Response
from python.api.project_common import ProjectCommon
import os

from python.helpers.print_style import PrintStyle


class ProjectDelete(ApiHandler):
    
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
            
            # 删除项目文件
            os.remove(project_file)
            
            return {
                "success": True,
                "message": f"Project {project_id} deleted successfully"
            }
            
        except Exception as e:
            PrintStyle().standard(f"[ProjectDelete] Error: {e}")
            return {
                "success": False,
                "error": str(e)
            }