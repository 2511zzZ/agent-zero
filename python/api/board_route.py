from python.helpers.api import ApiHandler
from flask import Request, Response, send_from_directory, render_template_string
import os


class BoardRoute(ApiHandler):
    async def process(self, input: dict, request: Request) -> Response:
        """处理Board UI路由"""
        
        # 检查是否有构建的Board UI文件
        board_ui_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'webui', 'board')
        
        if os.path.exists(board_ui_path):
            # 返回构建的静态文件
            return send_from_directory(board_ui_path, 'index.html')
        else:
            # 返回开发模式的重定向页面
            return Response(self._get_dev_redirect_html(), mimetype='text/html')
    
    def _get_dev_redirect_html(self) -> str:
        """返回开发模式重定向页面"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Board UI - Development Mode</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }
        .container {
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .redirect-link {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 24px;
            background: #3B82F6;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            transition: background 0.2s;
        }
        .redirect-link:hover {
            background: #2563EB;
        }
        .info {
            color: #666;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Board UI - Development Mode</h1>
        <p class="info">The Board UI is running in development mode.</p>
        <p class="info">Click the link below to access the development server:</p>
        <a href="http://localhost:3001" class="redirect-link" target="_blank">
            Open Board UI (Port 3001)
        </a>
        <p style="margin-top: 30px; font-size: 14px; color: #888;">
            If you're in production mode, the Board UI should be built and served automatically.
        </p>
    </div>
    
    <script>
        // 自动检测开发服务器是否可用
        fetch('http://localhost:3001')
            .then(() => {
                // 如果可用，显示成功消息
                console.log('Board UI dev server is available');
            })
            .catch(() => {
                // 如果不可用，显示错误消息
                const container = document.querySelector('.container');
                container.innerHTML += '<p style="color: red; margin-top: 20px;">⚠️ Development server not detected. Please check Docker logs.</p>';
            });
    </script>
</body>
</html>
        """.strip()