#!/usr/bin/env python3

import json
import time
import os

def update_board_version():
    """更新一些board数据的版本号以触发UI更新"""
    
    # 找到一个现有的新格式board文件
    test_files = [
        "memory/board_test_context.json",
        "memory/board_demo_board.json", 
        "memory/board_real_time_test.json"
    ]
    
    for board_file in test_files:
        if os.path.exists(board_file):
            print(f"📊 Updating {board_file}...")
            
            # 读取现有数据
            with open(board_file, 'r') as f:
                board_data = json.load(f)
            
            # 增加版本号并更新时间戳
            old_version = board_data.get('version', 1)
            board_data['version'] = old_version + 1
            board_data['metadata']['updated_at'] = time.time()
            
            # 添加一个新的测试节点
            new_node_id = f"updated-node-{int(time.time())}"
            board_data['nodes'][new_node_id] = {
                "id": new_node_id,
                "type": "note",
                "name": f"Updated Node {old_version + 1}",
                "description": f"This node was added to trigger version {old_version + 1} update",
                "status": "pending",
                "priority": "low",
                "position": {"x": 50 + (old_version * 30), "y": 400},
                "size": {"width": 200, "height": 120},
                "color": "#10B981",
                "content": {
                    "text": f"Version {old_version + 1} update test",
                    "artifacts": [],
                    "links": [],
                    "tags": ["update-test"],
                    "metadata": {"version": old_version + 1}
                },
                "parent_id": None,
                "children_ids": [],
                "dependencies": [],
                "created_at": time.time(),
                "updated_at": time.time()
            }
            
            # 保存更新的数据
            with open(board_file, 'w') as f:
                json.dump(board_data, f, indent=2)
            
            print(f"✅ Updated {board_file} to version {board_data['version']}")
            print(f"   - Added node: {new_node_id}")
            print(f"   - Total nodes: {len(board_data['nodes'])}")

def create_real_time_demo():
    """创建一个专门用于演示实时更新的board"""
    
    demo_context = "real_time_demo"
    board_file = f"memory/board_{demo_context}.json"
    
    board_data = {
        "version": 1,
        "nodes": {
            "demo-step-1": {
                "id": "demo-step-1",
                "type": "plan",
                "name": "Step 1: Initialize",
                "description": "Initialize the real-time demo board",
                "status": "completed",
                "priority": "high",
                "position": {"x": 100, "y": 100},
                "size": {"width": 220, "height": 160},
                "color": "#3B82F6",
                "content": {
                    "text": "This is the first step of our demo",
                    "artifacts": [],
                    "links": [],
                    "tags": ["demo", "step-1"],
                    "metadata": {}
                },
                "parent_id": None,
                "children_ids": ["demo-step-2"],
                "dependencies": [],
                "created_at": time.time(),
                "updated_at": time.time()
            },
            "demo-step-2": {
                "id": "demo-step-2",
                "type": "milestone",
                "name": "Step 2: Real-time Updates",
                "description": "Demonstrate real-time board updates",
                "status": "in_progress",
                "priority": "medium",
                "position": {"x": 400, "y": 150},
                "size": {"width": 200, "height": 150},
                "color": "#F59E0B",
                "content": {
                    "text": "This step shows real-time polling in action",
                    "artifacts": [],
                    "links": [],
                    "tags": ["demo", "step-2", "real-time"],
                    "metadata": {}
                },
                "parent_id": "demo-step-1",
                "children_ids": [],
                "dependencies": ["demo-step-1"],
                "created_at": time.time(),
                "updated_at": time.time()
            }
        },
        "connections": {
            "demo-conn-1": {
                "id": "demo-conn-1",
                "source_id": "demo-step-1",
                "target_id": "demo-step-2",
                "type": "parent_child",
                "label": "leads to",
                "style": {
                    "color": "#059669",
                    "width": 2,
                    "dash": []
                }
            }
        },
        "viewport": {"x": 0, "y": 0, "scale": 1},
        "layout": {
            "grid_size": 20,
            "snap_to_grid": True,
            "auto_layout": False
        },
        "metadata": {
            "title": "Real-time Demo Board",
            "description": "Board for demonstrating real-time updates",
            "tags": ["demo", "real-time", "polling"],
            "created_at": time.time(),
            "updated_at": time.time(),
            "last_editor": "demo-script"
        }
    }
    
    with open(board_file, 'w') as f:
        json.dump(board_data, f, indent=2)
    
    print(f"🎯 Created demo board: {board_file}")
    print(f"   - Context ID: {demo_context}")
    print(f"   - Version: {board_data['version']}")
    print(f"   - Nodes: {len(board_data['nodes'])}")
    print(f"   - Connections: {len(board_data['connections'])}")

if __name__ == "__main__":
    print("🚀 Triggering board updates for real-time demo...")
    
    # 更新现有board
    update_board_version()
    
    print()
    
    # 创建演示board
    create_real_time_demo()
    
    print()
    print("💡 Tips for testing:")
    print("1. Open board UI: http://localhost:50080/board.html")
    print("2. Check browser console for polling logs")
    print("3. Run this script again to see real-time updates")
    print("4. Use context 'real_time_demo' for demo board")