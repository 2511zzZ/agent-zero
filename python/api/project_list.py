from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers import files
from python.api.project_common import ProjectCommon
import json
import os

from python.helpers.print_style import PrintStyle


class ProjectList(ApiHandler):
    
    @classmethod
    def get_methods(cls) -> list[str]:
        return ["GET"]
    
    async def process(self, input: dict, request: Request) -> dict | Response:
        try:
            # 确保项目目录存在
            projects_dir = ProjectCommon.ensure_projects_dir()
            
            projects = []
            
            # 读取所有项目文件
            if os.path.exists(projects_dir):
                project_files = [f for f in os.listdir(projects_dir) if f.endswith('.json')]
                
                for filename in project_files:
                    project_file = os.path.join(projects_dir, filename)
                    
                    try:
                        # 读取并解析项目文件
                        project_data = files.read_file(project_file)
                        project = json.loads(project_data)
                        
                        # 规范化项目数据
                        project = ProjectCommon.normalize_project(project)
                        projects.append(project)
                        
                    except json.JSONDecodeError as e:
                        PrintStyle().standard(f"[ProjectList] Invalid JSON in {filename}: {e}")
                        continue
                    except Exception as e:
                        PrintStyle().standard(f"[ProjectList] Error loading {filename}: {e}")
                        continue
            
            # 按更新时间排序
            projects.sort(key=lambda x: x.get('updatedAt', 0), reverse=True)
            
            return {
                "success": True,
                "projects": projects,
                "total": len(projects)
            }
            
        except Exception as e:
            PrintStyle().standard(f"[ProjectList] Error: {e}")
            return {
                "success": False,
                "error": str(e),
                "projects": [],
                "total": 0
            }