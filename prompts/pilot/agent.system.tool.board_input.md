# Board Input Tool (BoardInputTool)

This tool is used to receive and process human modifications made on the board (such as adjusting plans, editing/adding/deleting nodes). All edit requests should be handled, and the agent's subsequent plans and outputs must be updated accordingly to reflect human intent.

## Input data structure:
- edits: list of board edit actions
  - action: string ("add", "update", "delete")
  - item: board item object (see BoardOutputTool)
- user_id: string (who made the edit)

### Example usage:
~~~json
{
    "thoughts": [
        "Apply human's changes to the board: update plan, delete old note."
    ],
    "tool_name": "board_input",
    "tool_args": {
        "edits": [
            {
                "action": "update",
                "item": {
                    "id": "plan-001",
                    "type": "plan",
                    "content": "Step 1: Collect requirements. Step 2: Design solution. Step 3: Review.",
                    "metadata": {"priority": "high"}
                }
            },
            {
                "action": "delete",
                "item": {
                    "id": "note-001",
                    "type": "note",
                    "content": "Old note to be removed."
                }
            }
        ],
        "user_id": "human-123"
    }
}
~~~

## Output:
- message: string, summary of board update
- break_loop: boolean 