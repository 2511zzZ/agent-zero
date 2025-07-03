# Board Output Tool (BoardOutputTool)

This tool is used to output the current plan, key steps, and artifacts as structured information to the shared board. Each invocation should include the latest plan, key nodes, and outputs, ensuring the board remains up-to-date and traceable for human review.

## Input data structure:
- items: list of board items (plan, artifact, note, etc.)
  - id: unique string
  - type: string (e.g. "plan", "artifact", "note")
  - content: string
  - metadata: object (optional)
    - For artifacts, you can include a `file` field with a file link (e.g. URL or relative path) to reference the actual file, instead of just text.

### Example usage:
~~~json
{
    "thoughts": [
        "Update the board with the latest plan and key artifacts."
    ],
    "tool_name": "board_output",
    "tool_args": {
        "items": [
            {
                "id": "plan-001",
                "type": "plan",
                "content": "Step 1: Collect requirements. Step 2: Design solution.",
                "metadata": {"priority": "high"}
            },
            {
                "id": "artifact-001",
                "type": "artifact",
                "content": "Initial design diagram uploaded.",
                "metadata": {"file": "/files/design.png", "description": "Design diagram"}
            }
        ]
    }
}
~~~

## Output:
- message: string, summary of board update
- break_loop: boolean 