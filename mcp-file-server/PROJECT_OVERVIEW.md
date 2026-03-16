# File Operations MCP Server - Project Overview

## 🎯 What is This?

This is a **Model Context Protocol (MCP) server** that gives Claude Desktop powerful file system capabilities. Once configured, Claude can:

- 📂 Browse directories
- 📄 Read and write files
- 🔍 Search for files and content
- 📊 Get file metadata
- 🗑️ Safely delete files

## 📁 Project Structure

```
mcp-file-server/
├── server.py                    # Main MCP server implementation
├── test_server.py              # Test script to verify functionality
├── setup.sh                    # Automated setup script (Linux/macOS)
├── requirements.txt            # Python dependencies
├── README.md                   # Full documentation
├── QUICKSTART.md              # Quick start guide
├── PROJECT_OVERVIEW.md        # This file
├── claude_config_example.json # Example Claude configuration
└── .gitignore                 # Git ignore rules
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
cd mcp-file-server
./setup.sh
```

This will:
1. Create a Python virtual environment
2. Install dependencies
3. Run tests
4. Show you the configuration to add to Claude

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install mcp

# Test it works
python3 test_server.py
```

Then add to your Claude config file (see below).

## ⚙️ Configuration

### Claude Desktop Config Location

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Config Content

```json
{
  "mcpServers": {
    "file-ops": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-file-server/server.py"]
    }
  }
}
```

**⚠️ Important**: Use the **absolute path** to server.py!

## 🛠️ Available Tools

### 1. list_directory
List all files and directories in a path.

**Example**: "List the files in the src directory"

### 2. read_file
Read the contents of a text file.

**Example**: "Read the README.md file"

### 3. write_file
Create or overwrite a file with content.

**Example**: "Write a new config.json file with these settings..."

### 4. search_files
Find files matching a glob pattern (recursive).

**Example**: "Search for all Python files in the project"

### 5. file_info
Get detailed metadata about a file (size, dates, hash, permissions).

**Example**: "Show me information about setup.py"

### 6. create_directory
Create a new directory (and parent directories if needed).

**Example**: "Create a directory called output"

### 7. delete_file
Delete a file (not directories, for safety).

**Example**: "Delete the temporary.log file"

### 8. grep_files
Search for text content within files (like Unix grep).

**Example**: "Find all TODO comments in Python files"

## 🧪 Testing

### Run Test Suite

```bash
python3 test_server.py
```

This creates a test_output directory with sample files and tests all operations.

### Test with MCP Inspector

```bash
npx @anthropics/mcp-inspector python3 server.py
```

Opens a web UI where you can test tools interactively.

### Manual Protocol Test

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}' | python3 server.py
```

## 🔒 Security Considerations

1. **File Access**: The server has the same file system permissions as the user running it
2. **Path Safety**: Uses Path.resolve() to prevent path traversal attacks
3. **Delete Safety**: Only allows file deletion (not directories)
4. **Read Limits**: MD5 hashing limited to files < 100MB

## 🐛 Troubleshooting

### Server Not Showing in Claude

1. ✅ Check path in config is absolute
2. ✅ Verify Python 3 is installed: `python3 --version`
3. ✅ Confirm MCP is installed: `pip list | grep mcp`
4. ✅ Restart Claude Desktop completely

### "No module named 'mcp'"

```bash
cd mcp-file-server
source venv/bin/activate
pip install mcp
```

### Permission Errors

```bash
chmod +x server.py
```

## 📚 Technical Details

### Architecture

- **Protocol**: MCP (Model Context Protocol) 2024-11-05
- **Transport**: stdio (standard input/output)
- **Language**: Python 3.7+
- **Framework**: MCP SDK 1.x

### How It Works

1. Claude Desktop launches the server as a subprocess
2. Communicates via JSON-RPC over stdin/stdout
3. Claude discovers available tools via `tools/list`
4. Claude calls tools via `tools/call` with parameters
5. Server executes operations and returns results

### Code Structure

```python
# Server initialization
server = Server("file-ops-server")

# Tool registration
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    # Returns tool definitions with JSON schemas

# Tool execution
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    # Routes to appropriate function and returns results
```

## 🔧 Customization

### Add a New Tool

1. Create an async function:
```python
async def my_new_tool(param: str) -> list[types.TextContent]:
    """Tool description."""
    result = f"Processed: {param}"
    return [types.TextContent(type="text", text=result)]
```

2. Add to tool list in `handle_list_tools()`:
```python
types.Tool(
    name="my_new_tool",
    description="Description of what it does",
    inputSchema={
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
)
```

3. Add to tool router in `handle_call_tool()`:
```python
elif name == "my_new_tool":
    return await my_new_tool(**arguments)
```

## 📖 Learn More

- **MCP Documentation**: https://modelcontextprotocol.io
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **MCP Specification**: https://spec.modelcontextprotocol.io

## 🤝 Contributing

Ideas for improvements:
- Add binary file support
- Implement file watching
- Add compression/archive tools
- Include git integration
- Add file comparison features

## 📄 License

MIT License - Free to use and modify!

## 🎉 Success!

If you've completed the setup:
1. ✅ Server is installed
2. ✅ Tests pass
3. ✅ Claude config is updated
4. ✅ Claude Desktop is restarted

Try asking Claude: **"List the files in the current directory"**

Enjoy your enhanced Claude with file operations! 🚀
