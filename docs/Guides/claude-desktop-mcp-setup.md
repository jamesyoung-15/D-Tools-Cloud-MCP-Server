# Adding MCP Server to Claude Desktop

## Setup Instructions

1. Click on user profile typically in bottom lefthand corner
2. Go to settings
3. Click on `Developer` tab
4. Click `Edit Config` button, this should open a configuration JSON file (eg. `claude_desktop_config.json`)
5. Add the following to the JSON file

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

    make sure to replace the `replace-me` with the full directory path, eg:

    - Windows: `C:\\Users\\myuser\\Documents\\D-Tools-Cloud-MCP-Server`
    - Mac: `~/Downloads/D-Tools-Cloud-MCP-Server`

6. Restart Claude Desktop, make sure to fully quit not just close window

7. After re-opening Claude Desktop, it should work, you can test it by asking a question in chat related to D-Tools
