# File Operations MCP Server

A powerful MCP server that provides Claude with file and directory operation capabilities.

## Features

This MCP server exposes the following tools:

### 📁 Directory Operations
- **list_directory**: List contents of a directory with file sizes
- **create_directory**: Create new directories (with parent support)
- **search_files**: Search for files using glob patterns (e.g., `*.py`, `test_*.txt`)

### 📄 File Operations
- **read_file**: Read text file contents with encoding support
- **write_file**: Write or overwrite files (creates directories as needed)
- **delete_file**: Delete files (directories excluded for safety)
- **file_info**: Get detailed file/directory metadata (size, permissions, hash, etc.)

### 🔍 Search Operations
- **grep_files**: Search for text content within files (like Unix grep)

## Installation

1. **Create virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Make server executable**:
   ```bash
   chmod +x server.py
   ```

## Configuration

### For Claude Desktop

Add to your Claude configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

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

**Important**: Replace `/absolute/path/to/mcp-file-server/server.py` with the actual absolute path to your server.py file.

### For Cline (VS Code Extension)

Add to Cline's MCP settings:

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

## Testing

### Test with MCP Inspector

```bash
# Install MCP Inspector (if not already installed)
npm install -g @anthropics/mcp-inspector

# Run inspector
mcp-inspector python3 server.py
```

This will open a web interface where you can test all the tools interactively.

### Manual Testing

You can also test the server directly:

```bash
# Test listing tools
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 server.py

# Test reading a file
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"read_file","arguments":{"path":"README.md"}}}' | python3 server.py
```

## Usage Examples

Once configured, you can ask Claude things like:

- "List the files in the current directory"
- "Read the contents of config.json"
- "Search for all Python files in the project"
- "Find all occurrences of 'TODO' in .py files"
- "Create a new directory called 'output'"
- "Write a JSON file with the following content..."
- "Get detailed information about setup.py"

## Security Notes

⚠️ **Important Security Considerations**:

1. **File System Access**: This server has access to the file system with the same permissions as the user running it
2. **Path Traversal**: While the server uses Path.resolve() to handle paths safely, be aware of what directories you're working in
3. **Delete Operations**: The `delete_file` tool only deletes files, not directories, as a safety measure
4. **File Size Limits**: MD5 hashing is only performed on files smaller than 100MB to avoid performance issues

## Troubleshooting

### Server Not Appearing in Claude

1. Check that the path in the config is absolute (not relative)
2. Verify Python 3 is installed: `python3 --version`
3. Ensure MCP package is installed: `pip list | grep mcp`
4. Restart Claude Desktop completely

### Permission Errors

If you get permission errors:
- Make sure server.py is executable: `chmod +x server.py`
- Check that you have read/write permissions for directories you're accessing

### Import Errors

If you see "No module named 'mcp'":
```bash
pip install mcp
```

## Development

To add new tools:

1. Add a new function decorated with `@server.tool()`
2. Include a docstring describing the tool and its parameters
3. Use type hints for all parameters
4. Return strings (can be JSON formatted for structured data)

Example:
```python
@server.tool()
async def my_new_tool(param1: str, param2: int = 10) -> str:
    """Brief description of what the tool does.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter (default: 10)
    """
    # Your implementation
    return "Result"
```

## License

MIT License - Feel free to modify and use as needed!

## Contributing

Contributions are welcome! Some ideas for enhancements:
- Add support for binary file operations
- Implement file comparison tools
- Add archive/compression operations (zip, tar)
- Include git operations integration
- Add file watching capabilities
