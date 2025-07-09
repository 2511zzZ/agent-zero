"""
项目管理公共逻辑
提供项目相关 API 的通用功能
"""

import os
import time
from python.helpers.print_style import PrintStyle


class ProjectCommon:
    """项目管理公共功能类"""
    
    @staticmethod
    def get_projects_dir() -> str:
        """获取正确的项目目录路径"""
        # 检测是否在 Docker 容器中
        if os.path.exists('/.dockerenv') or os.getcwd() == '/':
            # 在容器中，使用 /a0/memory/projects
            return "/a0/memory/projects"
        else:
            # 在开发环境中，使用相对路径
            return "memory/projects"
    
    @staticmethod
    def ensure_projects_dir() -> str:
        """确保项目目录存在并返回路径"""
        projects_dir = ProjectCommon.get_projects_dir()
        
        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)
            PrintStyle().standard(f"[ProjectCommon] Created projects directory: {projects_dir}")
        
        return projects_dir
    
    @staticmethod
    def get_project_file_path(project_id: str) -> str:
        """获取项目文件的完整路径"""
        projects_dir = ProjectCommon.get_projects_dir()
        return os.path.join(projects_dir, f"{project_id}.json")
    
    @staticmethod
    def normalize_project(project: dict) -> dict:
        """规范化项目数据，确保包含所有必要字段"""
        now = time.time()
        
        # 基本字段
        project.setdefault('id', project.get('id', ''))
        project.setdefault('name', project.get('name', 'Untitled Project'))
        project.setdefault('description', project.get('description', ''))
        project.setdefault('status', project.get('status', 'active'))
        project.setdefault('createdAt', project.get('createdAt', now))
        project.setdefault('updatedAt', project.get('updatedAt', now))
        
        # 画板数据
        if 'flowchart' not in project:
            project['flowchart'] = {
                'nodes': [],
                'edges': [],
                'viewport': {'x': 0, 'y': 0, 'zoom': 1},
                'version': 0
            }
        
        # 聊天历史
        if 'chatHistory' not in project:
            project['chatHistory'] = []
        
        return project
    
    @staticmethod
    def is_container_environment() -> bool:
        """检测是否在容器环境中运行"""
        return os.path.exists('/.dockerenv') or os.getcwd() == '/' 