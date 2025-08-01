# 师门任务 MCP Server

This MCP server exposes the existing 师门任务 (Shimen Task) game automation as a tool that can be controlled by AI assistants like Claude Desktop.

## Quick Start

### 1. Install Dependencies

```bash
cd mcp_game_automation_server
pip install -r requirements.txt
```

### 2. Test the Server

```bash
# Test directly
python server.py

# Or test with MCP development tools
uv run mcp dev server.py
```

**MCP Inspector Manual Configuration:**

If the auto-detection doesn't work, manually configure in the MCP Inspector:

- **Transport Type:** `stdio`
- **Command:** `/Users/kx/game_automation_project/venv/bin/python3`
- **Arguments:** `/Users/kx/game_automation_project/mcp_game_automation_server/server.py`
- **Working Directory:** `/Users/kx/game_automation_project`

### 3. Claude Desktop Integration

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "shimen_task_automation": {
      "command": "python",
      "args": ["/Users/kx/game_automation_project/mcp_game_automation_server/server.py"],
      "cwd": "/Users/kx/game_automation_project"
    }
  }
}
```

## Available Tools

### `run_shimen_task`

Executes the complete 师门任务 automation sequence.

**Parameters:**
- `verbose` (optional, boolean): If true, returns detailed output from the automation script

**Returns:**
- `success`: Boolean indicating if automation completed successfully
- `output`: Output from the automation script (truncated unless verbose=true)
- `execution_time_seconds`: Time taken to execute
- `error_message`: Error details if execution failed

## Usage Examples

### Via AI Assistant
```
User: "Run my 师门任务 automation"
AI: [Calls run_shimen_task tool]
Result: "✅ 师门任务 automation completed successfully in 45 seconds"
```

### Via MCP Inspector
```bash
uv run mcp dev server.py
# Then call run_shimen_task() in the inspector
```

## Architecture

```
AI Assistant (Claude) 
    ↓ MCP Protocol
MCP Server (server.py)
    ↓ subprocess call
run_shimen_task.sh
    ↓ executes
action_automation.py → MuMu Emulator
```

The MCP server is a lightweight wrapper that:
1. Receives tool calls from AI assistants via MCP protocol
2. Executes the existing `run_shimen_task.sh` script
3. Returns structured results back to the AI

## Project Structure

```
mcp_game_automation_server/
├── server.py              # Main MCP server
├── requirements.txt       # Dependencies  
└── README.md              # This file

# Existing automation (unchanged):
├── run_shimen_task.sh     # Shell script wrapper
├── action_automation.py   # Main automation engine
├── config.py             # Action plans and coordinates
└── game_elements/        # UI templates
```

## Benefits

- ✅ **AI Control**: Ask AI to run automation on demand
- ✅ **No Changes**: Existing automation scripts unchanged
- ✅ **Standardized**: Uses MCP protocol for interoperability  
- ✅ **Structured Results**: Get detailed success/failure feedback
- ✅ **Timeout Protection**: 5-minute timeout prevents hanging

## Troubleshooting

### Server Won't Start
- Check that `run_shimen_task.sh` exists in the parent directory
- Verify MCP dependencies are installed: `pip install "mcp[cli]"`
- Ensure you're in the correct directory

### Automation Fails
- Test the original automation: `./run_shimen_task.sh`
- Check logs in `shimen_task.log`
- Verify MuMu emulator and game are properly configured
- Check macOS permissions (screen recording, accessibility)

### MCP Connection Issues
- Restart Claude Desktop after config changes
- Check JSON syntax in Claude Desktop config
- Verify file paths are absolute and correct

### MCP Inspector Issues
If MCP Inspector auto-detection fails, manually configure:

```
Transport: stdio
Command: /Users/kx/game_automation_project/venv/bin/python3
Arguments: /Users/kx/game_automation_project/mcp_game_automation_server/server.py
Working Directory: /Users/kx/game_automation_project
```

**Note:** Don't use the auto-suggested `uv` commands if you don't have `uv` installed. 