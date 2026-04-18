# Adding MCP Server to Claude Desktop

## Setup Instructions

1. Click on user profile typically in bottom lefthand corner
2. Go to settings
3. Click on `Developer` tab
4. Click `Edit Config` button, this should open a configuration JSON file (eg. `claude_desktop_config.json`)
5. Add the following to the JSON file, make sure to replace `replace-me` with the full path to this directory, eg: `C:\\Users\\myuser\\Documents\\D-Tools-Cloud-MCP-Server` on Windows, `~/Downloads/D-Tools-Cloud-MCP-Server` on Mac:

```json
{
    "mcpServers": {
        "d-tools-cloud": {
            "command": "uv",
            "args": [
                "--directory",
                "replace-me",
                "run",
                "main.py"
            ]
        }
    }
}
```

6. Restart Claude Desktop, make sure to fully quit not just close window

7. After re-opening Claude Desktop, it should work, you can test it by asking a question in chat related to D-Tools
