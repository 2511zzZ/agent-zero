from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers import files
from python.api.project_common import ProjectCommon
import json
import os
import time

from python.helpers.print_style import PrintStyle


class ProjectUpdate(ApiHandler):
    
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
            
            # 读取现有项目数据
            project_data = files.read_file(project_file)
            project = json.loads(project_data)
            
            # 更新项目字段
            if 'name' in input and input['name'].strip():
                project['name'] = input['name'].strip()
            
            if 'description' in input:
                project['description'] = input['description'].strip()
            
            if 'status' in input:
                project['status'] = input['status']
            
            if 'flowchart' in input:
                project['flowchart'] = input['flowchart']
                # 更新版本号
                project['flowchart']['version'] = project['flowchart'].get('version', 0) + 1
            
            if 'chatHistory' in input:
                project['chatHistory'] = input['chatHistory']
            
            # 更新时间戳
            project['updatedAt'] = time.time()
            
            # 保存更新的项目
            files.write_file(project_file, json.dumps(project, indent=2))
            
            return {
                "success": True,
                "project": project
            }
            
        except json.JSONDecodeError as e:
            project_id = input.get('project_id', 'unknown')
            PrintStyle().standard(f"[ProjectUpdate] Invalid JSON for project {project_id}: {e}")
            return {
                "success": False,
                "error": "Invalid project data format"
            }
        except Exception as e:
            PrintStyle().standard(f"[ProjectUpdate] Error: {e}")
            return {
                "success": False,
                "error": str(e)
            }