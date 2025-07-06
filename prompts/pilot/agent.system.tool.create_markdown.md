# Create Markdown Tool (CreateMarkdownTool)

该工具用于根据输入内容创建 markdown 文件，并返回可访问的文件链接。适用于保存笔记、文档、计划等结构化文本。

## 输入数据结构:
- content: string，markdown 格式的内容
- filename: string，可选，文件名（如 my_note.md），默认为 note.md

### 示例用法:
~~~json
{
    "thoughts": [
        "保存会议记录为 markdown 文件。"
    ],
    "tool_name": "create_markdown",
    "tool_args": {
        "content": "# 会议纪要\n- 讨论项目进展\n- 确定下周目标",
        "filename": "meeting_notes.md"
    }
}
~~~

## 输出:
- message: string，包含 markdown 文件的 Web 访问链接
- break_loop: boolean 