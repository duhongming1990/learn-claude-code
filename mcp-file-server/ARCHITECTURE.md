# MCP Server Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Desktop                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  User: "List files in the current directory"           │    │
│  └────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         Claude analyzes request & decides to           │    │
│  │         use 'list_directory' tool                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             │ JSON-RPC over stdio
                             │
┌────────────────────────────┼─────────────────────────────────────┐
│                            ▼                                     │
│                  MCP Server (server.py)                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  1. Receives: tools/call request                       │    │
│  │     {"name": "list_directory", "arguments": {...}}     │    │
│  └────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  2. Routes to list_directory() function                │    │
│  └────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  3. Executes file system operation                     │    │
│  │     - Resolves path                                    │    │
│  │     - Reads directory contents                         │    │
│  │     - Formats results                                  │    │
│  └────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  4. Returns: [TextContent]                             │    │
│  │     "FILE  1024  config.json\nFILE  2048  README.md"   │    │
│  └────────────────────────────────────────────────────────┘    │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │ JSON-RPC response
                             │
┌────────────────────────────┼─────────────────────────────────────┐
│                            ▼                                     │
│                      Claude Desktop                              │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Claude receives result and formats response:          │    │
│  │  "I found the following files in the directory:        │    │
│  │   - config.json (1024 bytes)                           │    │
│  │   - README.md (2048 bytes)"                            │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Claude Desktop (Client)

**Role**: User interface and AI agent

**Responsibilities**:
- Receives user requests
- Analyzes which tools are needed
- Constructs tool call requests
- Formats responses for users

**Configuration File**: `claude_desktop_config.json`
```json
{
  "mcpServers": {
    "file-ops": {
      "command": "python3",
      "args": ["/path/to/server.py"]
    }
  }
}
```

### 2. MCP Server (server.py)

**Role**: Tool provider and executor

**Key Components**:

#### a. Server Instance
```python
server = Server("file-ops-server")
```

#### b. Tool Registration Handler
```python
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_directory",
            description="...",
            inputSchema={...}
        ),
        # ... more tools
    ]
```

#### c. Tool Execution Handler
```python
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "list_directory":
        return await list_directory(**arguments)
    # ... route to other tools
```

#### d. Tool Implementation Functions
```python
async def list_directory(path: str = ".") -> list[types.TextContent]:
    # Actual file system operations
    dir_path = Path(path).resolve()
    items = list(dir_path.iterdir())
    # Format and return results
    return [types.TextContent(type="text", text=result)]
```

### 3. Communication Protocol

**Protocol**: JSON-RPC 2.0 over stdio

**Key Message Types**:

#### Initialize
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "claude", "version": "1.0"}
  }
}
```

#### List Tools
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

#### Call Tool
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "list_directory",
    "arguments": {"path": "/home/user/projects"}
  }
}
```

## Data Flow

### Tool Discovery Flow

```
┌─────────────┐         initialize        ┌─────────────┐
│   Claude    │ ────────────────────────> │     MCP     │
│   Desktop   │                            │   Server    │
│             │ <──────────────────────── │             │
└─────────────┘    serverInfo + caps      └─────────────┘
       │                                          
       │           tools/list                     
       │ ─────────────────────────────────────> │
       │                                          
       │ <───────────────────────────────────── │
       │         list of all tools               
       │    (names, descriptions, schemas)       
```

### Tool Execution Flow

```
┌─────────────┐      tools/call           ┌─────────────┐
│   Claude    │ ────────────────────────> │     MCP     │
│   Desktop   │   {name, arguments}        │   Server    │
│             │                            │             │
│             │                            │   ┌──────┐  │
│             │                            │   │ Tool │  │
│             │                            │   │ Exec │  │
│             │                            │   └──────┘  │
│             │                            │      │      │
│             │                            │      ▼      │
│             │                            │  ┌────────┐ │
│             │                            │  │  File  │ │
│             │                            │  │ System │ │
│             │                            │  └────────┘ │
│             │                            │      │      │
│             │ <──────────────────────── │      ▼      │
│             │      [TextContent]         │   result    │
└─────────────┘                            └─────────────┘
```

## Security Model

### Sandboxing

```
┌──────────────────────────────────────────────────┐
│            File System Access                     │
│                                                   │
│  ┌─────────────────────────────────────────┐    │
│  │  MCP Server runs with user permissions  │    │
│  │  - Can access user's files              │    │
│  │  - Cannot escalate privileges           │    │
│  │  - Respects OS file permissions         │    │
│  └─────────────────────────────────────────┘    │
│                                                   │
│  Security Features:                              │
│  ✓ Path.resolve() prevents traversal            │
│  ✓ No directory deletion                        │
│  ✓ File size limits for hashing                 │
│  ✓ Error handling for permissions               │
└──────────────────────────────────────────────────┘
```

### Trust Boundary

```
 Untrusted                 Trusted
┌─────────┐              ┌─────────┐              ┌─────────┐
│  User   │    Claude    │   MCP   │  File Ops   │  File   │
│  Input  │  validates   │  Server │  validated  │ System  │
│         │ ──────────> │         │ ──────────> │         │
└─────────┘   context    └─────────┘   paths     └─────────┘
                             │
                             │ All paths resolved
                             │ All inputs validated
                             ▼
                        Safe Operations
```

## Extension Points

### Adding New Tools

```
1. Implement Function
   ┌────────────────────────────────┐
   │ async def new_tool(params):    │
   │     # Logic here                │
   │     return [TextContent(...)]   │
   └────────────────────────────────┘
                │
                ▼
2. Register Tool
   ┌────────────────────────────────┐
   │ @server.list_tools()            │
   │ async def handle_list_tools():  │
   │     return [                    │
   │         Tool(name="new_tool",   │
   │              description="...", │
   │              inputSchema={...}) │
   │     ]                           │
   └────────────────────────────────┘
                │
                ▼
3. Route Calls
   ┌────────────────────────────────┐
   │ @server.call_tool()             │
   │ async def handle_call_tool(...):│
   │     if name == "new_tool":      │
   │         return await new_tool() │
   └────────────────────────────────┘
```

### Adding Resources

```python
@server.list_resources()
async def handle_list_resources():
    return [
        types.Resource(
            uri="file:///config",
            name="Configuration",
            description="App configuration"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str):
    if uri == "file:///config":
        return [types.TextContent(
            type="text",
            text=load_config()
        )]
```

## Performance Considerations

### Async Operations

```
Single Request Processing:
┌────────────────────────────────────┐
│ 1. Receive request                  │  ~1ms
│ 2. Validate & route                 │  ~1ms
│ 3. File system operation            │  ~5-50ms
│ 4. Format response                  │  ~1ms
│ 5. Send response                    │  ~1ms
└────────────────────────────────────┘
Total: ~10-55ms per operation
```

### Optimization Tips

1. **Use async/await**: Don't block event loop
2. **Limit result sizes**: Cap max_results parameters
3. **Stream large files**: For files > 1MB
4. **Cache metadata**: For frequently accessed info
5. **Batch operations**: Group related file ops

## Deployment Options

### Local Development
```
User's Machine
├── Claude Desktop App
└── MCP Server (Python process)
    └── Direct file system access
```

### Remote Server (Future)
```
User's Machine          Remote Server
├── Claude Desktop  ──► ├── MCP Server
└── Network requests     └── File system access
```

## Monitoring & Debugging

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def list_directory(path: str):
    logger.info(f"Listing directory: {path}")
    try:
        result = perform_operation()
        logger.info(f"Success: {len(result)} items")
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

### Testing Layers

```
1. Unit Tests
   ┌────────────────────┐
   │ Test each function │
   │ independently      │
   └────────────────────┘

2. Integration Tests
   ┌────────────────────┐
   │ Test tool handlers │
   │ with real FS ops   │
   └────────────────────┘

3. Protocol Tests
   ┌────────────────────┐
   │ Test JSON-RPC      │
   │ communication      │
   └────────────────────┘

4. End-to-End Tests
   ┌────────────────────┐
   │ Test with actual   │
   │ Claude Desktop     │
   └────────────────────┘
```

## Summary

The MCP File Operations Server is a clean, modular system that:

- ✅ Follows MCP specification
- ✅ Uses async/await for performance
- ✅ Validates all inputs
- ✅ Provides clear error messages
- ✅ Easy to extend with new tools
- ✅ Safe file system operations

Perfect for giving Claude powerful file manipulation capabilities! 🚀
