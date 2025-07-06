# Board Output Tool (BoardOutputTool)

该工具用于输出和更新当前的计划、每个节点的关键产物，以及最终产物。每次调用支持增量修改，所有内容会实时合并并持久化。

## 输入数据结构:
- plan: 计划节点列表（可选，增量更新）
  - id: string，节点唯一标识
  - name: string，节点名称
  - description: string，节点描述
  - artifacts: list，每个节点的关键产物（如为文件，需提供 file 字段，值为可访问链接）
    - type: string，产物类型（如 file、note 等）
    - name: string，产物名称
    - file: string，可选，文件 Web 链接
    - 其他自定义字段
- final_artifacts: list，最终产物（可选，增量更新，结构同上）

### 示例用法:
~~~json
{
    "thoughts": [
        "输出完整计划和初步产物。"
    ],
    "tool_name": "board_output",
    "tool_args": {
        "plan": [
            {
                "id": "step-1",
                "name": "需求收集",
                "description": "收集所有相关需求",
                "artifacts": []
            },
            {
                "id": "step-2",
                "name": "方案设计",
                "description": "设计整体解决方案",
                "artifacts": [
                    {
                        "type": "file",
                        "name": "design.png",
                        "file": "/files/design.png"
                    }
                ]
            }
        ],
        "final_artifacts": [
            {
                "type": "file",
                "name": "final_report.md",
                "file": "/files/final_report.md"
            }
        ]
    }
}
~~~

- 支持只更新部分节点或产物（如只追加某节点产物或最终产物）。
- 每次调用后，board 状态会合并并持久化。

## 输出:
- message: string，包含计划节点数和最终产物数
- break_loop: boolean 

## 注意事项
- chat_id 必须与主 chat 保持一致，建议每次调用时显式传递 chat_id 参数（如从 context.id 获取）。 