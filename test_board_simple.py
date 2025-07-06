#!/usr/bin/env python3

import json
import time
import os

def create_test_board_data():
    """创建测试board数据，模拟board_output工具的输出"""
    
    board_data = {
        "version": 2,  # 增加版本号以触发更新
        "nodes": {
            "agent-plan-1": {
                "id": "agent-plan-1",
                "type": "plan",
                "name": "Agent Generated Plan",
                "description": "This plan was created by the agent using board_output tool",
                "status": "in_progress",
                "priority": "high",
                "position": {"x": 200, "y": 150},
                "size": {"width": 220, "height": 160},
                "color": "#3B82F6",
                "content": {
                    "text": "Agent created this plan to demonstrate real-time updates",
                    "artifacts": [],
                    "links": [],
                    "tags": ["agent-generated"],
                    "metadata": {}
                },
                "parent_id": None,
                "children_ids": [],
                "dependencies": [],
                "created_at": time.time(),
                "updated_at": time.time()
            },
            "agent-milestone-1": {
                "id": "agent-milestone-1", 
                "type": "milestone",
                "name": "Real-time Update Test",
                "description": "Testing if board UI shows real-time updates",
                "status": "completed",
                "priority": "medium",
                "position": {"x": 500, "y": 200},
                "size": {"width": 200, "height": 150},
                "color": "#F59E0B",
                "content": {
                    "text": "This milestone tests the polling mechanism",
                    "artifacts": [],
                    "links": [],
                    "tags": ["test", "real-time"],
                    "metadata": {}
                },
                "parent_id": None,
                "children_ids": [],
                "dependencies": ["agent-plan-1"],
                "created_at": time.time(),
                "updated_at": time.time()
            }
        },
        "connections": {
            "conn-1": {
                "id": "conn-1",
                "source_id": "agent-plan-1",
                "target_id": "agent-milestone-1", 
                "type": "dependency",
                "label": "leads to",
                "style": {
                    "color": "#666666",
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
            "title": "Agent Generated Board",
            "description": "Board created by agent to test real-time updates",
            "tags": ["test", "agent", "real-time"],
            "created_at": time.time(),
            "updated_at": time.time(),
            "last_editor": "agent"
        }
    }
    
    return board_data

def save_board_data(context_id, board_data):
    """保存board数据到文件"""
    os.makedirs("memory", exist_ok=True)
    
    board_file = f"memory/board_{context_id}.json"
    with open(board_file, 'w') as f:
        json.dump(board_data, f, indent=2)
    
    print(f"✅ Board data saved to {board_file}")
    print(f"📊 Contains {len(board_data['nodes'])} nodes, {len(board_data['connections'])} connections")

def simulate_board_output_call():
    """模拟agent调用board_output工具"""
    print("🤖 Simulating agent board_output tool call...")
    
    # 模拟不同的context ID来测试
    test_contexts = ["test_context", "demo_board", "real_time_test"]
    
    for context_id in test_contexts:
        print(f"\n📝 Creating board for context: {context_id}")
        
        board_data = create_test_board_data()
        
        # 为每个context添加不同的节点
        board_data["nodes"][f"context-specific-{context_id}"] = {
            "id": f"context-specific-{context_id}",
            "type": "note",
            "name": f"Note for {context_id}",
            "description": f"This is a context-specific note for {context_id}",
            "status": "pending",
            "priority": "low",
            "position": {"x": 100, "y": 300},
            "size": {"width": 180, "height": 120},
            "color": "#FACC15",
            "content": {
                "text": f"Context: {context_id}",
                "artifacts": [],
                "links": [],
                "tags": [context_id],
                "metadata": {"context": context_id}
            },
            "parent_id": None,
            "children_ids": [],
            "dependencies": [],
            "created_at": time.time(),
            "updated_at": time.time()
        }
        
        save_board_data(context_id, board_data)
    
    print("\n🎯 All test boards created!")
    print("💡 Now you can:")
    print("  1. Open board UI in browser")
    print("  2. Watch for real-time updates")
    print("  3. Check console logs for polling activity")

if __name__ == "__main__":
    simulate_board_output_call()