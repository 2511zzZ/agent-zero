# Create Markdown Tool (CreateMarkdownTool)

Create and save markdown files for documentation, notes, reports, and structured text content.
Automatically generates web-accessible links for created files.
Supports various content types including meeting notes, project documentation, technical specifications, and more.
Files are saved to the work directory and can be accessed via the web interface.
Use proper markdown formatting for headings, lists, code blocks, tables, and other elements.
Content can include text, code snippets, images, links, and other markdown elements.
Tool returns a web link to access the created file immediately.

Usage:

1 Create meeting notes
~~~json
{
    "thoughts": [
        "Creating meeting notes with..."
    ],
    "tool_name": "create_markdown",
    "tool_args": {
        "content": "# Meeting Notes - Project Review...",
        "filename": "meeting_notes_2024_01_15.md"
    }
}
~~~

2 Create report with data and analysis
~~~json
{
    "thoughts": [
        "Creating comprehensive report with..."
    ],
    "tool_name": "create_markdown",
    "tool_args": {
        "content": "# Monthly Sales Report - January 2024\n\n## Executive Summary\nSales performance exceeded targets by 15% with total revenue of $125,000...",
        "filename": "sales_report_jan_2024.md"
    }
}
~~~

## Input Parameters:
- **content**: string (required) - Markdown formatted content to save
- **filename**: string (optional) - Custom filename with .md extension (defaults to "note.md")

## Output:
- **message**: string - Success message with web-accessible file link
- **break_loop**: boolean - Tool completion status 