#!/usr/bin/env python3

import sys
import json
import asyncio
from unittest.mock import Mock

# 添加项目根目录到路径
sys.path.append('.')

from python.tools.board_output_enhanced import BoardOutputEnhancedTool


class MockAgent:
    def __init__(self):
        self.context = Mock()
        self.context.id = "test_context"


async def test_board_output():
    print("🧪 Testing Board Output Enhanced Tool...")
    
    # 创建模拟的工具实例
    tool = BoardOutputEnhancedTool()
    tool.agent = MockAgent()
    
    # 测试创建节点
    test_nodes = [
        {
            "id": "node-1",
            "type": "plan",
            "name": "Test Plan Node",
            "description": "This is a test plan node created by the tool",
            "status": "pending",
            "priority": "high",
            "position": {"x": 150, "y": 100},
            "color": "#3B82F6"
        },
        {
            "id": "node-2", 
            "type": "milestone",
            "name": "Test Milestone",
            "description": "This is a test milestone",
            "status": "in_progress",
            "priority": "medium",
            "position": {"x": 400, "y": 150},
            "color": "#F59E0B"
        }
    ]
    
    # 执行board output操作
    try:
        result = await tool.execute(
            operation='update',
            nodes=test_nodes,
            metadata={"title": "Test Board from Tool", "description": "Created by test script"},
            chat_id="test_context"
        )
        
        print("✅ Board output tool executed successfully!")
        print(f"Result: {result.message}")
        
        # 验证文件是否创建
        import os
        board_file = "memory/board_test_context.json"
        if os.path.exists(board_file):
            print(f"✅ Board file created: {board_file}")
            
            # 读取并显示内容
            with open(board_file, 'r') as f:
                board_data = json.load(f)
                print("📊 Board data:")
                print(f"  - Nodes: {len(board_data['nodes'])}")
                print(f"  - Version: {board_data['version']}")
                print(f"  - Title: {board_data['metadata']['title']}")
                
                for node_id, node in board_data['nodes'].items():
                    print(f"  - {node['type']}: {node['name']} @ ({node['position']['x']}, {node['position']['y']})")
        else:
            print("❌ Board file not created")
            
    except Exception as e:
        print(f"❌ Error executing board output tool: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_board_output())