# Quick Start Guide

Get your MCP server running in 3 minutes!

## 🚀 Quick Setup

### Step 1: Run Setup Script

```bash
cd mcp-file-server
./setup.sh
```

This will:
- Create a Python virtual environment
- Install required dependencies
- Run tests to verify everything works
- Display configuration instructions

### Step 2: Configure Claude

Copy the configuration shown at the end of setup and add it to your Claude config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

If the file doesn't exist, create it with this content (replace the path):

```json
{
  "mcpServers": {
    "file-ops": {
      "command": "python3",
      "args": ["/full/path/to/mcp-file-server/server.py"]
    }
  }
}
```

### Step 3: Restart Claude

Completely quit and restart Claude Desktop.

### Step 4: Test It!

Try asking Claude:
- "List the files in the current directory"
- "Read the README.md file"
- "Search for all Python files in this project"

## 🎯 What You Can Do

### File Operations
```
"Read the contents of config.json"
"Write a new file called output.txt with these contents: ..."
"Delete the temporary.log file"
```

### Directory Operations
```
"List all files in the src directory"
"Create a new directory called output"
"Search for all .py files in the project"
```

### Search Operations
```
"Find all occurrences of 'TODO' in Python files"
"Search for 'import' in all .py files"
"Show me files that contain 'error' or 'exception'"
```

### Information
```
"Get detailed information about setup.py"
"Show me the size and modification date of config.json"
```

## 🔧 Troubleshooting

### "Server not found" in Claude

1. Check the path in your config is **absolute** (starts with `/` or `C:\`)
2. Verify the path is correct: `ls /path/to/server.py`
3. Restart Claude completely (don't just close the window)

### "No module named 'mcp'"

```bash
cd mcp-file-server
source venv/bin/activate  # Or: venv\Scripts\activate on Windows
pip install mcp
```

### Test Without Claude

```bash
cd mcp-file-server
source venv/bin/activate
python3 test_server.py
```

### Use MCP Inspector

See all available tools and test them interactively:

```bash
npx @anthropics/mcp-inspector python3 /path/to/server.py
```

## 📚 Learn More

- Read the full [README.md](README.md) for detailed documentation
- Check out [server.py](server.py) to see how tools are implemented
- Visit [MCP Documentation](https://modelcontextprotocol.io) for protocol details

## 💡 Tips

1. **Always use absolute paths** in Claude config
2. **Test with test_server.py** before configuring Claude
3. **Use MCP Inspector** to debug tool calls
4. **Check Claude's developer logs** if tools aren't appearing
5. **Restart Claude** after any config changes

Happy coding! 🎉
