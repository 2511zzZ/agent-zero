import sys
import os
import asyncio
import time
import json
import uuid

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from python.tools.board_output_enhanced import BoardOutputEnhancedTool
from python.helpers import files


class MockAgent:
    """模拟Agent对象"""
    def __init__(self, context_id="test_board"):
        self.context = type('Context', (), {'id': context_id})()


class BoardOutputTester:
    """Board Output工具测试器"""
    
    def __init__(self):
        self.tool = BoardOutputEnhancedTool()
        self.tool.agent = MockAgent()
        self.test_cases = []
        self.results = []
        
    def add_test_case(self, name, description, test_data):
        """添加测试用例"""
        self.test_cases.append({
            'name': name,
            'description': description,
            'data': test_data
        })
    
    async def run_test(self, test_case):
        """运行单个测试"""
        print(f"\n🧪 Running test: {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        
        try:
            result = await self.tool.execute(**test_case['data'])
            print(f"   ✅ Success: {result.message}")
            return True
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("🚀 Starting board_output enhanced tool tests...")
        print("=" * 60)
        
        results = []
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n[{i}/{len(self.test_cases)}]", end=" ")
            success = await self.run_test(test_case)
            results.append(success)
            
            # 短暂延迟，让输出更清晰
            await asyncio.sleep(0.1)
            
        print(f"\n" + "=" * 60)
        print(f"📊 Test Results: {sum(results)}/{len(results)} passed")
        
        if sum(results) == len(results):
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the output above.")
            
        return results


def create_test_cases():
    """创建测试用例"""
    tester = BoardOutputTester()
    
    # 测试1: 创建初始计划
    tester.add_test_case(
        "create_initial_plan",
        "创建包含3个阶段的初始项目计划",
        {
            "operation": "create",
            "nodes": [
                {
                    "id": "phase-1",
                    "type": "plan",
                    "name": "需求分析",
                    "description": "收集和分析项目需求",
                    "status": "pending",
                    "priority": "high",
                    "position": {"x": 100, "y": 100},
                    "color": "#EF4444",
                    "content": {
                        "artifacts": [],
                        "tags": ["requirements", "analysis"]
                    }
                },
                {
                    "id": "phase-2",
                    "type": "milestone",
                    "name": "系统设计",
                    "description": "设计系统架构和技术方案",
                    "status": "pending",
                    "priority": "high",
                    "position": {"x": 100, "y": 300},
                    "color": "#F59E0B",
                    "content": {
                        "artifacts": [],
                        "tags": ["design", "architecture"]
                    }
                },
                {
                    "id": "phase-3",
                    "type": "deliverable",
                    "name": "开发实现",
                    "description": "编码实现和单元测试",
                    "status": "pending",
                    "priority": "medium",
                    "position": {"x": 100, "y": 500},
                    "color": "#10B981",
                    "content": {
                        "artifacts": [],
                        "tags": ["development", "coding"]
                    }
                }
            ]
        }
    )
    
    # 测试2: 添加产物
    tester.add_test_case(
        "add_artifacts",
        "为第一阶段添加需求文档和原型",
        {
            "operation": "update",
            "nodes": [
                {
                    "id": "phase-1",
                    "content": {
                        "artifacts": [
                            {
                                "id": str(uuid.uuid4()),
                                "type": "document",
                                "name": "需求规格说明书",
                                "description": "详细的功能需求文档",
                                "file_path": "/files/requirements.md",
                                "metadata": {"version": "1.0", "author": "产品经理"},
                                "created_at": time.time(),
                                "updated_at": time.time()
                            },
                            {
                                "id": str(uuid.uuid4()),
                                "type": "link",
                                "name": "交互原型",
                                "description": "Figma设计原型",
                                "url": "https://figma.com/proto/123",
                                "metadata": {"tool": "figma", "version": "v1.0"},
                                "created_at": time.time(),
                                "updated_at": time.time()
                            }
                        ]
                    }
                }
            ]
        }
    )
    
    # 测试3: 创建节点连接
    tester.add_test_case(
        "create_connections",
        "创建阶段间的依赖关系",
        {
            "operation": "connect",
            "connections": [
                {
                    "id": "conn-1",
                    "source_id": "phase-1",
                    "target_id": "phase-2",
                    "type": "dependency",
                    "label": "需求完成后开始设计",
                    "style": {"color": "#3B82F6", "width": 2}
                },
                {
                    "id": "conn-2",
                    "source_id": "phase-2",
                    "target_id": "phase-3",
                    "type": "dependency",
                    "label": "设计完成后开始开发",
                    "style": {"color": "#3B82F6", "width": 2}
                }
            ]
        }
    )
    
    # 测试4: 更新节点状态
    tester.add_test_case(
        "update_status",
        "将第一阶段标记为进行中",
        {
            "operation": "update",
            "nodes": [
                {
                    "id": "phase-1",
                    "status": "in_progress",
                    "color": "#3B82F6",
                    "content": {
                        "metadata": {"started_at": time.time()}
                    }
                }
            ]
        }
    )
    
    # 测试5: 增量更新
    tester.add_test_case(
        "incremental_update",
        "增量添加新产物，不影响现有产物",
        {
            "operation": "update",
            "nodes": [
                {
                    "id": "phase-1",
                    "content": {
                        "artifacts": [
                            {
                                "id": str(uuid.uuid4()),
                                "type": "note",
                                "name": "用户故事集",
                                "description": "整理的用户故事和验收标准",
                                "content": "作为用户，我希望能够...",
                                "metadata": {"priority": "high"},
                                "created_at": time.time(),
                                "updated_at": time.time()
                            }
                        ]
                    }
                }
            ]
        }
    )
    
    # 测试6: 创建便签节点
    tester.add_test_case(
        "create_note_node",
        "创建一个便签节点用于记录想法",
        {
            "operation": "create",
            "nodes": [
                {
                    "id": "note-1",
                    "type": "note",
                    "name": "项目想法",
                    "description": "临时记录和想法",
                    "status": "pending",
                    "priority": "low",
                    "position": {"x": 400, "y": 100},
                    "color": "#FACC15",
                    "content": {
                        "text": "这里是一些关于项目的临时想法和备注。\n\n可以多行文本。",
                        "tags": ["idea", "brainstorm"],
                        "artifacts": []
                    }
                }
            ]
        }
    )
    
    # 测试7: 更新视图状态
    tester.add_test_case(
        "update_viewport",
        "更新画布视图状态",
        {
            "operation": "update",
            "viewport": {
                "x": -100,
                "y": -50,
                "scale": 0.8
            },
            "metadata": {
                "title": "测试项目计划",
                "description": "这是一个用于测试的项目计划",
                "last_editor": "tester"
            }
        }
    )
    
    # 测试8: 删除节点
    tester.add_test_case(
        "delete_node",
        "删除便签节点",
        {
            "operation": "delete",
            "nodes": [
                {"id": "note-1"}
            ]
        }
    )
    
    return tester


async def main():
    """主函数"""
    print("🔧 Agent Zero Board Output Enhanced Tool Tests")
    print("=" * 60)
    
    # 创建测试器
    tester = create_test_cases()
    
    # 运行所有测试
    results = await tester.run_all_tests()
    
    # 显示最终board状态
    print(f"\n📋 Final Board State:")
    print("-" * 40)
    try:
        board_data = files.read_file("memory/board_test_board.json")
        board_state = json.loads(board_data)
        
        # 显示统计信息
        node_count = len(board_state.get('nodes', {}))
        conn_count = len(board_state.get('connections', {}))
        version = board_state.get('version', 0)
        
        print(f"📊 Statistics:")
        print(f"   Nodes: {node_count}")
        print(f"   Connections: {conn_count}")
        print(f"   Version: {version}")
        print(f"   Last Updated: {time.ctime(board_state.get('metadata', {}).get('updated_at', 0))}")
        
        # 显示节点类型分布
        if node_count > 0:
            type_counts = {}
            for node in board_state['nodes'].values():
                node_type = node.get('type', 'unknown')
                type_counts[node_type] = type_counts.get(node_type, 0) + 1
            
            print(f"\n📈 Node Types:")
            for node_type, count in type_counts.items():
                print(f"   {node_type}: {count}")
        
        # 显示完整的JSON（格式化）
        print(f"\n📄 Complete Board JSON:")
        print("-" * 40)
        print(json.dumps(board_state, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Cannot read board state: {e}")
    
    print(f"\n🏁 Test execution completed!")
    return results


if __name__ == "__main__":
    # 运行测试
    results = asyncio.run(main())
    
    # 设置退出码
    exit_code = 0 if all(results) else 1
    sys.exit(exit_code)