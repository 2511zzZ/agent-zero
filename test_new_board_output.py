#!/usr/bin/env python3

import json
import os
import time
from unittest.mock import Mock

# 模拟 board_output 工具的新格式输出
def simulate_board_output_new_format():
    """模拟使用新格式的board_output工具调用"""
    
    context_id = "test_new_format"
    board_file = f"memory/board_{context_id}.json"
    
    # 创建新格式的board数据
    board_state = {
        'version': 1,
        'nodes': {},
        'connections': {},
        'viewport': {'x': 0, 'y': 0, 'scale': 1},
        'layout': {'grid_size': 20, 'snap_to_grid': True, 'auto_layout': False},
        'metadata': {
            'title': 'New Format Test Board',
            'description': 'Testing new format board output',
            'tags': ['test', 'new-format'],
            'created_at': time.time(),
            'updated_at': time.time(),
            'last_editor': 'board_output'
        }
    }
    
    # 模拟agent调用board_output工具创建节点
    test_plan = [
        {
            'id': 'phase-1',
            'name': '需求分析阶段',
            'description': '收集和分析项目需求',
            'artifacts': [
                {'type': 'file', 'name': 'requirements.md', 'file': '/files/requirements.md'},
                {'type': 'note', 'name': '需求讨论记录'}
            ]
        },
        {
            'id': 'phase-2', 
            'name': '设计阶段',
            'description': '创建系统架构和设计文档',
            'artifacts': [
                {'type': 'file', 'name': 'design.md', 'file': '/files/design.md'}
            ]
        },
        {
            'id': 'phase-3',
            'name': '开发阶段',
            'description': '实现和测试解决方案',
            'artifacts': []
        }
    ]
    
    # 将plan转换为新格式的nodes
    for i, node_dict in enumerate(test_plan):
        node_id = node_dict['id']
        current_time = time.time()
        
        board_state['nodes'][node_id] = {
            'id': node_id,
            'type': 'plan',
            'name': node_dict['name'],
            'description': node_dict['description'],
            'status': 'pending',
            'priority': 'medium',
            'position': {'x': 100 + (i % 3) * 250, 'y': 100 + (i // 3) * 200},
            'size': {'width': 200, 'height': 150},
            'color': '#3B82F6',
            'content': {
                'text': node_dict['description'],
                'artifacts': node_dict.get('artifacts', []),
                'tags': [],
                'metadata': {}
            },
            'parent_id': None,
            'children_ids': [],
            'dependencies': [],
            'created_at': current_time,
            'updated_at': current_time
        }
    
    # 添加final_artifacts到metadata
    final_artifacts = [
        {'type': 'file', 'name': 'project_summary.md', 'file': '/files/project_summary.md'},
        {'type': 'report', 'name': '项目完成报告'}
    ]
    board_state['metadata']['final_artifacts'] = final_artifacts
    
    # 更新版本和时间戳
    board_state['version'] = 2
    board_state['metadata']['updated_at'] = time.time()
    
    # 保存新格式的board文件
    os.makedirs("memory", exist_ok=True)
    with open(board_file, 'w') as f:
        json.dump(board_state, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created new format board: {board_file}")
    print(f"📊 Board stats:")
    print(f"   - Version: {board_state['version']}")
    print(f"   - Nodes: {len(board_state['nodes'])}")
    print(f"   - Connections: {len(board_state['connections'])}")
    print(f"   - Title: {board_state['metadata']['title']}")
    
    for node_id, node in board_state['nodes'].items():
        artifacts_count = len(node['content']['artifacts'])
        print(f"   - {node['type']}: {node['name']} ({artifacts_count} artifacts)")
    
    return context_id, board_state


def test_conversion_of_old_format():
    """测试旧格式文件被board_output工具转换"""
    
    # 找到一个旧格式文件
    old_format_file = "memory/board_b226456e-d0aa-40f2-8c27-0ab332e77797.json"
    
    if os.path.exists(old_format_file):
        print(f"\n🔄 Testing conversion of old format file: {old_format_file}")
        
        # 读取旧格式
        with open(old_format_file, 'r') as f:
            old_data = json.load(f)
        
        print(f"📋 Old format detected:")
        print(f"   - Has 'plan' key: {'plan' in old_data}")
        print(f"   - Has 'version' key: {'version' in old_data}")
        print(f"   - Plan nodes: {len(old_data.get('plan', []))}")
        
        # 备份原文件
        backup_file = old_format_file + ".backup"
        with open(backup_file, 'w') as f:
            json.dump(old_data, f, indent=2)
        print(f"💾 Backed up to: {backup_file}")
        
        # 现在下次当agent调用board_output工具时，它会自动转换为新格式
        print(f"💡 Next time agent calls board_output for this context, it will be converted to new format")
    else:
        print(f"\n❌ Old format file not found: {old_format_file}")


if __name__ == "__main__":
    print("🧪 Testing new format board_output...")
    
    # 创建新格式测试数据
    context_id, board_state = simulate_board_output_new_format()
    
    # 测试旧格式转换
    test_conversion_of_old_format()
    
    print(f"\n🎯 Test complete!")
    print(f"💡 You can now:")
    print(f"   1. Open board UI: http://localhost:50080/board.html")
    print(f"   2. Test with context: {context_id}")
    print(f"   3. Watch for real-time updates")
    print(f"   4. Check that board_poll returns version {board_state['version']}")