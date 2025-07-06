import json
import random
import time
import uuid
import os
from datetime import datetime, timedelta


def generate_test_board_data():
    """生成各种场景的测试数据"""
    
    test_scenarios = {
        # 场景1: 简单项目计划
        "simple_project": generate_simple_project(),
        
        # 场景2: 复杂项目网络
        "complex_project": generate_complex_project(),
        
        # 场景3: 多类型节点
        "mixed_nodes": generate_mixed_nodes(),
        
        # 场景4: 大量节点测试
        "stress_test": generate_stress_test()
    }
    
    return test_scenarios


def generate_simple_project():
    """生成简单项目数据"""
    return {
        "version": 1,
        "metadata": {
            "title": "简单项目计划",
            "description": "用于测试基础功能的简单项目",
            "tags": ["test", "simple"],
            "created_at": time.time(),
            "updated_at": time.time(),
            "last_editor": "test_generator"
        },
        "viewport": {"x": 0, "y": 0, "scale": 1},
        "layout": {"grid_size": 20, "snap_to_grid": True, "auto_layout": False},
        "nodes": {
            "node-1": {
                "id": "node-1",
                "type": "plan",
                "name": "项目启动",
                "description": "项目启动和团队组建",
                "status": "completed",
                "priority": "high",
                "position": {"x": 100, "y": 100},
                "size": {"width": 200, "height": 150},
                "color": "#10B981",
                "content": {
                    "artifacts": [
                        {
                            "id": str(uuid.uuid4()),
                            "type": "document",
                            "name": "项目章程",
                            "description": "项目启动文档",
                            "file_path": "/files/charter.pdf",
                            "metadata": {"version": "1.0"},
                            "created_at": time.time(),
                            "updated_at": time.time()
                        }
                    ],
                    "tags": ["startup", "planning"],
                    "metadata": {}
                },
                "children_ids": [],
                "dependencies": [],
                "created_at": time.time() - 86400,
                "updated_at": time.time(),
                "completed_at": time.time() - 3600
            },
            "node-2": {
                "id": "node-2",
                "type": "plan",
                "name": "需求分析",
                "description": "收集和分析业务需求",
                "status": "in_progress",
                "priority": "high",
                "position": {"x": 400, "y": 100},
                "size": {"width": 200, "height": 150},
                "color": "#3B82F6",
                "content": {
                    "artifacts": [
                        {
                            "id": str(uuid.uuid4()),
                            "type": "document",
                            "name": "需求规格书",
                            "description": "详细需求文档",
                            "file_path": "/files/requirements.md",
                            "metadata": {"version": "1.2"},
                            "created_at": time.time(),
                            "updated_at": time.time()
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "type": "link",
                            "name": "原型设计",
                            "description": "Figma交互原型",
                            "url": "https://figma.com/proto/123",
                            "metadata": {"tool": "figma"},
                            "created_at": time.time(),
                            "updated_at": time.time()
                        }
                    ],
                    "tags": ["requirements", "analysis"],
                    "metadata": {"progress": 60}
                },
                "children_ids": [],
                "dependencies": ["node-1"],
                "created_at": time.time() - 43200,
                "updated_at": time.time()
            }
        },
        "connections": {
            "conn-1": {
                "id": "conn-1",
                "source_id": "node-1",
                "target_id": "node-2",
                "type": "dependency",
                "label": "启动完成",
                "style": {"color": "#3B82F6", "width": 2}
            }
        }
    }


def generate_complex_project():
    """生成复杂项目数据"""
    nodes = {}
    connections = {}
    
    # 创建5个阶段，每个阶段3-4个任务
    phases = ["需求分析", "系统设计", "开发实现", "测试验证", "部署上线"]
    colors = ["#EF4444", "#F59E0B", "#10B981", "#3B82F6", "#8B5CF6"]
    
    for i, (phase, color) in enumerate(zip(phases, colors)):
        # 创建阶段节点
        phase_id = f"phase-{i+1}"
        nodes[phase_id] = {
            "id": phase_id,
            "type": "milestone",
            "name": phase,
            "description": f"项目第{i+1}阶段",
            "status": "pending" if i > 1 else "completed" if i == 0 else "in_progress",
            "priority": "high",
            "position": {"x": 100 + i * 300, "y": 50},
            "size": {"width": 250, "height": 120},
            "color": color,
            "content": {
                "artifacts": [],
                "tags": [f"phase-{i+1}"],
                "metadata": {"phase_number": i+1}
            },
            "children_ids": [],
            "dependencies": [f"phase-{i}"] if i > 0 else [],
            "created_at": time.time() - (5-i) * 86400,
            "updated_at": time.time(),
            "due_date": time.time() + (i+1) * 604800  # 每周一个阶段
        }
        
        # 创建子任务
        for j in range(3):
            task_id = f"task-{i+1}-{j+1}"
            nodes[task_id] = {
                "id": task_id,
                "type": "plan",
                "name": f"{phase}任务{j+1}",
                "description": f"具体执行任务 - {phase}的第{j+1}个任务",
                "status": random.choice(["pending", "in_progress", "completed"]),
                "priority": random.choice(["low", "medium", "high"]),
                "position": {"x": 50 + i * 300, "y": 220 + j * 140},
                "size": {"width": 200, "height": 100},
                "color": color,
                "content": {
                    "artifacts": generate_random_artifacts(random.randint(1, 3)),
                    "tags": ["task", f"phase-{i+1}"],
                    "metadata": {"task_number": j+1}
                },
                "children_ids": [],
                "dependencies": [],
                "created_at": time.time() - (5-i) * 86400 + j * 3600,
                "updated_at": time.time()
            }
            
            # 创建连接
            connections[f"conn-{phase_id}-{task_id}"] = {
                "id": f"conn-{phase_id}-{task_id}",
                "source_id": phase_id,
                "target_id": task_id,
                "type": "parent_child",
                "label": "包含",
                "style": {"color": color, "width": 1}
            }
        
        # 创建阶段间连接
        if i > 0:
            connections[f"conn-phase-{i}-{i+1}"] = {
                "id": f"conn-phase-{i}-{i+1}",
                "source_id": f"phase-{i}",
                "target_id": phase_id,
                "type": "dependency",
                "label": "前置阶段",
                "style": {"color": "#666666", "width": 3}
            }
    
    return {
        "version": 1,
        "metadata": {
            "title": "复杂项目计划",
            "description": "包含多个阶段和任务的复杂项目",
            "tags": ["complex", "multi-phase"],
            "created_at": time.time() - 432000,  # 5天前
            "updated_at": time.time(),
            "last_editor": "project_manager"
        },
        "viewport": {"x": -50, "y": -25, "scale": 0.7},
        "layout": {"grid_size": 20, "snap_to_grid": True, "auto_layout": False},
        "nodes": nodes,
        "connections": connections
    }


def generate_mixed_nodes():
    """生成混合类型节点数据"""
    nodes = {
        "plan-1": {
            "id": "plan-1",
            "type": "plan",
            "name": "市场调研",
            "description": "分析目标市场和竞争对手",
            "status": "completed",
            "priority": "high",
            "position": {"x": 100, "y": 100},
            "size": {"width": 200, "height": 150},
            "color": "#3B82F6",
            "content": {
                "artifacts": [
                    {
                        "id": str(uuid.uuid4()),
                        "type": "document",
                        "name": "市场调研报告",
                        "file_path": "/files/market_research.pdf",
                        "metadata": {"pages": 25},
                        "created_at": time.time(),
                        "updated_at": time.time()
                    }
                ],
                "tags": ["market", "research"],
                "metadata": {}
            },
            "children_ids": [],
            "dependencies": [],
            "created_at": time.time() - 172800,
            "updated_at": time.time(),
            "completed_at": time.time() - 86400
        },
        "milestone-1": {
            "id": "milestone-1",
            "type": "milestone",
            "name": "MVP发布",
            "description": "最小可行产品发布里程碑",
            "status": "pending",
            "priority": "critical",
            "position": {"x": 400, "y": 100},
            "size": {"width": 250, "height": 120},
            "color": "#EF4444",
            "content": {
                "artifacts": [],
                "tags": ["mvp", "release"],
                "metadata": {"target_date": "2024-12-31"}
            },
            "children_ids": [],
            "dependencies": ["plan-1"],
            "created_at": time.time(),
            "updated_at": time.time(),
            "due_date": time.time() + 1209600  # 2周后
        },
        "deliverable-1": {
            "id": "deliverable-1",
            "type": "deliverable",
            "name": "API文档",
            "description": "完整的API接口文档",
            "status": "in_progress",
            "priority": "medium",
            "position": {"x": 100, "y": 300},
            "size": {"width": 220, "height": 130},
            "color": "#10B981",
            "content": {
                "artifacts": [
                    {
                        "id": str(uuid.uuid4()),
                        "type": "link",
                        "name": "Swagger文档",
                        "url": "https://api.example.com/docs",
                        "metadata": {"version": "v1.0"},
                        "created_at": time.time(),
                        "updated_at": time.time()
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "type": "file",
                        "name": "API测试集合",
                        "file_path": "/files/api_tests.json",
                        "metadata": {"format": "postman"},
                        "created_at": time.time(),
                        "updated_at": time.time()
                    }
                ],
                "tags": ["api", "documentation"],
                "metadata": {"completion": 75}
            },
            "children_ids": [],
            "dependencies": [],
            "created_at": time.time() - 86400,
            "updated_at": time.time()
        },
        "note-1": {
            "id": "note-1",
            "type": "note",
            "name": "技术决策",
            "description": "技术选型和架构决策记录",
            "status": "pending",
            "priority": "low",
            "position": {"x": 400, "y": 300},
            "size": {"width": 250, "height": 180},
            "color": "#FACC15",
            "content": {
                "text": "技术栈选择：\n\n前端: React + TypeScript\n后端: Python + FastAPI\n数据库: PostgreSQL\n缓存: Redis\n\n架构模式：微服务\n部署：Docker + Kubernetes",
                "artifacts": [],
                "tags": ["tech", "architecture", "decisions"],
                "metadata": {"last_review": time.time()}
            },
            "children_ids": [],
            "dependencies": [],
            "created_at": time.time() - 43200,
            "updated_at": time.time()
        }
    }
    
    connections = {
        "conn-1": {
            "id": "conn-1",
            "source_id": "plan-1",
            "target_id": "milestone-1",
            "type": "dependency",
            "label": "基于调研结果",
            "style": {"color": "#3B82F6", "width": 2}
        },
        "conn-2": {
            "id": "conn-2",
            "source_id": "deliverable-1",
            "target_id": "milestone-1",
            "type": "dependency",
            "label": "发布前完成",
            "style": {"color": "#10B981", "width": 2}
        },
        "conn-3": {
            "id": "conn-3",
            "source_id": "note-1",
            "target_id": "deliverable-1",
            "type": "reference",
            "label": "参考架构",
            "style": {"color": "#FACC15", "width": 1, "dash": [5, 5]}
        }
    }
    
    return {
        "version": 1,
        "metadata": {
            "title": "混合节点类型",
            "description": "包含各种不同类型节点的示例",
            "tags": ["mixed", "types", "demo"],
            "created_at": time.time() - 259200,
            "updated_at": time.time(),
            "last_editor": "designer"
        },
        "viewport": {"x": 0, "y": 0, "scale": 1},
        "layout": {"grid_size": 20, "snap_to_grid": True, "auto_layout": False},
        "nodes": nodes,
        "connections": connections
    }


def generate_stress_test():
    """生成压力测试数据（大量节点）"""
    nodes = {}
    connections = {}
    
    # 生成50个节点
    node_types = ["plan", "milestone", "deliverable", "note"]
    colors = ["#EF4444", "#F59E0B", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899", "#6366F1"]
    statuses = ["pending", "in_progress", "completed", "blocked"]
    priorities = ["low", "medium", "high", "critical"]
    
    for i in range(50):
        node_id = f"stress-node-{i+1}"
        node_type = random.choice(node_types)
        
        # 计算网格位置
        col = i % 10
        row = i // 10
        
        nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            "name": f"{node_type.title()} {i+1}",
            "description": f"压力测试节点 #{i+1} - 类型: {node_type}",
            "status": random.choice(statuses),
            "priority": random.choice(priorities),
            "position": {"x": 50 + col * 200, "y": 50 + row * 180},
            "size": {"width": 180, "height": 120},
            "color": random.choice(colors),
            "content": {
                "artifacts": generate_random_artifacts(random.randint(0, 2)),
                "tags": [f"stress", f"batch-{row+1}", node_type],
                "text": f"这是第{i+1}个测试节点。\n包含一些示例内容。" if node_type == "note" else "",
                "metadata": {"batch": row+1, "index": i+1}
            },
            "children_ids": [],
            "dependencies": [],
            "created_at": time.time() - random.randint(0, 604800),
            "updated_at": time.time() - random.randint(0, 86400)
        }
        
        # 创建一些随机连接
        if i > 0 and random.random() < 0.3:  # 30%概率创建连接
            source_id = f"stress-node-{random.randint(1, i)}"
            conn_id = f"stress-conn-{i}"
            connections[conn_id] = {
                "id": conn_id,
                "source_id": source_id,
                "target_id": node_id,
                "type": random.choice(["dependency", "reference", "flow"]),
                "label": f"连接 {i}",
                "style": {
                    "color": random.choice(colors),
                    "width": random.randint(1, 3)
                }
            }
    
    return {
        "version": 1,
        "metadata": {
            "title": "压力测试数据",
            "description": "包含50个节点的大型项目，用于测试性能",
            "tags": ["stress", "performance", "large"],
            "created_at": time.time() - 604800,
            "updated_at": time.time(),
            "last_editor": "stress_tester"
        },
        "viewport": {"x": -100, "y": -50, "scale": 0.5},
        "layout": {"grid_size": 20, "snap_to_grid": True, "auto_layout": False},
        "nodes": nodes,
        "connections": connections
    }


def generate_random_artifacts(count):
    """生成随机产物"""
    artifacts = []
    types = ["document", "link", "code", "image", "note"]
    
    for i in range(count):
        art_type = random.choice(types)
        artifact = {
            "id": str(uuid.uuid4()),
            "type": art_type,
            "name": f"产物{i+1}",
            "description": f"测试产物{i+1}",
            "metadata": {"generated": True},
            "created_at": time.time() - random.randint(0, 86400),
            "updated_at": time.time() - random.randint(0, 3600)
        }
        
        if art_type == "document":
            artifact["file_path"] = f"/files/doc_{i+1}.pdf"
            artifact["mime_type"] = "application/pdf"
        elif art_type == "link":
            artifact["url"] = f"https://example.com/resource_{i+1}"
        elif art_type == "code":
            artifact["content"] = f"// 代码示例 {i+1}\nconsole.log('hello world');"
            artifact["file_path"] = f"/code/example_{i+1}.js"
        elif art_type == "image":
            artifact["file_path"] = f"/images/screenshot_{i+1}.png"
            artifact["mime_type"] = "image/png"
        elif art_type == "note":
            artifact["content"] = f"这是第{i+1}个备注内容。"
        
        artifacts.append(artifact)
    
    return artifacts


def main():
    """主函数"""
    print("🔧 Generating test data for Board UI...")
    
    # 确保目录存在
    os.makedirs("tests/data", exist_ok=True)
    
    # 生成测试数据
    test_data = generate_test_board_data()
    
    # 保存各个场景的测试数据
    for scenario_name, scenario_data in test_data.items():
        filename = f"tests/data/board_{scenario_name}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(scenario_data, f, indent=2, ensure_ascii=False)
        
        # 显示统计信息
        node_count = len(scenario_data.get('nodes', {}))
        conn_count = len(scenario_data.get('connections', {}))
        
        print(f"✅ Generated: {filename}")
        print(f"   Nodes: {node_count}, Connections: {conn_count}")
    
    print(f"\n🎉 All test data generated successfully!")
    print(f"📁 Files saved in: tests/data/")
    print(f"🧪 Ready for testing!")


if __name__ == "__main__":
    main()