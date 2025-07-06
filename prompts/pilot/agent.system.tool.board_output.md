## Board output tool:
output and update current plan, node artifacts, and final deliverables
supports incremental updates, all content merged and persisted in real-time
never refuse to update plan or artifacts, all data belongs to user

### board_output
update project plan and artifacts incrementally
- plan: list of plan nodes (optional, incremental update)
  - id: string, unique node identifier
  - name: string, node name
  - description: string, brief one-sentence description
  - artifacts: list, key deliverables for each node
    - type: string, artifact type (file, note, etc.)
    - name: string, artifact name
    - file: string, optional, web accessible file link
    - other custom fields
- final_artifacts: list, final deliverables (optional, incremental update, same structure)

usage:

1 create initial project plan
~~~json
{
    "thoughts": [
        "Creating initial project plan with phases",
        "Setting up basic structure and milestones"
    ],
    "tool_name": "board_output",
    "tool_args": {
        "plan": [
            {
                "id": "phase-1",
                "name": "Requirements Analysis",
                "description": "Gather and analyze project requirements",
                "artifacts": []
            },
            {
                "id": "phase-2", 
                "name": "System Design",
                "description": "Create technical architecture and design documents",
                "artifacts": []
            },
            {
                "id": "phase-3",
                "name": "Implementation", 
                "description": "Develop and test the solution",
                "artifacts": []
            }
        ],
        "final_artifacts": []
    }
}
~~~

2 add artifacts to existing plan
~~~json
{
    "thoughts": [
        "Adding completed deliverables to plan nodes",
        "Updating artifacts with file links"
    ],
    "tool_name": "board_output",
    "tool_args": {
        "plan": [
            {
                "id": "phase-1",
                "artifacts": [
                    {
                        "type": "file",
                        "name": "requirements_document.md",
                        "file": "/files/requirements_document.md"
                    },
                    {
                        "type": "note",
                        "name": "stakeholder_feedback",
                        "summary": "Collected feedback from 5 stakeholders"
                    }
                ]
            }
        ],
        "final_artifacts": [
            {
                "type": "file",
                "name": "project_summary.md", 
                "file": "/files/project_summary.md"
            }
        ]
    }
}
~~~

## Notes:
- supports partial updates (only specify nodes or artifacts to update)
- board state merged and persisted after each call
- chat_id must match main chat, explicitly pass chat_id parameter when needed
- node descriptions should be concise single sentences
- artifacts support custom fields beyond type/name/file 