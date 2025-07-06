from python.helpers.tool import Tool, Response
from python.helpers import files
import os

class CreateMarkdownTool(Tool):
    async def execute(self, **kwargs):
        # content: markdown 内容
        # filename: 可选，文件名（不含路径），默认为 'note.md'
        # 中文注释：生成 markdown 文件并返回可访问的链接，路径包含 chat_id 防止冲突
        content = kwargs.get('content', '')
        filename = kwargs.get('filename', 'note.md')
        # 文件名安全处理
        filename = files.safe_file_name(filename)
        # 获取当前 chat_id，若无则用 'default'
        chat_id = getattr(self.agent.context, 'id', 'default')
        # 保存到 webui/public/files/{chat_id}/ 目录
        save_dir = os.path.join('webui/public/files', chat_id)
        os.makedirs(files.get_abs_path(save_dir), exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        print(f"save_path: {save_path}")
        files.write_file(save_path, content)
        # 构造 Web 访问链接
        file_link = f"/files/{chat_id}/{filename}"
        return Response(message=f"Markdown created: {file_link}", break_loop=False) 