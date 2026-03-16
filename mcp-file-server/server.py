#!/usr/bin/env python3
"""
File Operations MCP Server

This MCP server provides tools for file and directory operations,
making it easy for Claude to work with the filesystem.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Any
import asyncio

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp import types

# Create server instance
server = Server("file-ops-server")


async def list_directory(path: str = ".") -> list[types.TextContent]:
    """List contents of a directory."""
    try:
        dir_path = Path(path).resolve()
        if not dir_path.exists():
            return [types.TextContent(
                type="text",
                text=f"Error: Directory '{path}' does not exist"
            )]
        
        if not dir_path.is_dir():
            return [types.TextContent(
                type="text",
                text=f"Error: '{path}' is not a directory"
            )]
        
        items = []
        for item in sorted(dir_path.iterdir()):
            item_type = "DIR" if item.is_dir() else "FILE"
            size = item.stat().st_size if item.is_file() else 0
            items.append(f"{item_type:5} {size:>10} {item.name}")
        
        result = "\n".join([f"Directory: {dir_path}", "=" * 60] + items)
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def read_file(path: str, encoding: str = "utf-8") -> list[types.TextContent]:
    """Read contents of a text file."""
    try:
        file_path = Path(path).resolve()
        if not file_path.exists():
            return [types.TextContent(
                type="text",
                text=f"Error: File '{path}' does not exist"
            )]
        
        if not file_path.is_file():
            return [types.TextContent(
                type="text",
                text=f"Error: '{path}' is not a file"
            )]
        
        content = file_path.read_text(encoding=encoding)
        result = f"File: {file_path}\nSize: {len(content)} bytes\n{'-' * 60}\n{content}"
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def write_file(path: str, content: str, encoding: str = "utf-8") -> list[types.TextContent]:
    """Write content to a file (creates or overwrites)."""
    try:
        file_path = Path(path).resolve()
        
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_path.write_text(content, encoding=encoding)
        size = file_path.stat().st_size
        
        result = f"Success: Wrote {size} bytes to {file_path}"
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def search_files(directory: str, pattern: str, max_results: int = 50) -> list[types.TextContent]:
    """Search for files matching a pattern in a directory (recursive)."""
    try:
        dir_path = Path(directory).resolve()
        if not dir_path.exists():
            return [types.TextContent(
                type="text",
                text=f"Error: Directory '{directory}' does not exist"
            )]
        
        matches = []
        for match in dir_path.rglob(pattern):
            if len(matches) >= max_results:
                break
            relative = match.relative_to(dir_path)
            item_type = "DIR" if match.is_dir() else "FILE"
            size = match.stat().st_size if match.is_file() else 0
            matches.append(f"{item_type:5} {size:>10} {relative}")
        
        if not matches:
            result = f"No files matching '{pattern}' found in {directory}"
        else:
            header = f"Found {len(matches)} matches for '{pattern}' in {directory}:"
            result = "\n".join([header, "=" * 60] + matches)
        
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def file_info(path: str) -> list[types.TextContent]:
    """Get detailed information about a file or directory."""
    try:
        file_path = Path(path).resolve()
        if not file_path.exists():
            return [types.TextContent(
                type="text",
                text=f"Error: '{path}' does not exist"
            )]
        
        stat = file_path.stat()
        
        info = {
            "path": str(file_path),
            "name": file_path.name,
            "type": "directory" if file_path.is_dir() else "file",
            "size_bytes": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "permissions": oct(stat.st_mode)[-3:],
        }
        
        # Add file hash for files
        if file_path.is_file() and stat.st_size < 100_000_000:  # Only hash files < 100MB
            with open(file_path, 'rb') as f:
                info["md5"] = hashlib.md5(f.read()).hexdigest()
        
        return [types.TextContent(type="text", text=json.dumps(info, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def create_directory(path: str, parents: bool = True) -> list[types.TextContent]:
    """Create a new directory."""
    try:
        dir_path = Path(path).resolve()
        
        if dir_path.exists():
            return [types.TextContent(
                type="text",
                text=f"Error: '{path}' already exists"
            )]
        
        dir_path.mkdir(parents=parents, exist_ok=False)
        return [types.TextContent(type="text", text=f"Success: Created directory {dir_path}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def delete_file(path: str) -> list[types.TextContent]:
    """Delete a file (NOT directories, for safety)."""
    try:
        file_path = Path(path).resolve()
        
        if not file_path.exists():
            return [types.TextContent(
                type="text",
                text=f"Error: '{path}' does not exist"
            )]
        
        if file_path.is_dir():
            return [types.TextContent(
                type="text",
                text=f"Error: '{path}' is a directory. This tool only deletes files for safety."
            )]
        
        file_path.unlink()
        return [types.TextContent(type="text", text=f"Success: Deleted file {file_path}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def grep_files(directory: str, search_term: str, file_pattern: str = "*", 
                    case_sensitive: bool = False, max_results: int = 100) -> list[types.TextContent]:
    """Search for text content within files (like grep)."""
    try:
        dir_path = Path(directory).resolve()
        if not dir_path.exists():
            return [types.TextContent(
                type="text",
                text=f"Error: Directory '{directory}' does not exist"
            )]
        
        search_lower = search_term.lower() if not case_sensitive else search_term
        matches = []
        
        for file_path in dir_path.rglob(file_pattern):
            if not file_path.is_file():
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    check_line = line if case_sensitive else line.lower()
                    if search_lower in check_line:
                        relative = file_path.relative_to(dir_path)
                        matches.append(f"{relative}:{line_num}: {line.strip()}")
                        
                        if len(matches) >= max_results:
                            break
            except Exception:
                continue  # Skip files that can't be read
            
            if len(matches) >= max_results:
                break
        
        if not matches:
            result = f"No matches found for '{search_term}' in {directory}"
        else:
            header = f"Found {len(matches)} matches for '{search_term}':"
            result = "\n".join([header, "=" * 60] + matches)
        
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


# Register tools
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="list_directory",
            description="List contents of a directory with file sizes and types",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list (default: current directory)",
                        "default": "."
                    }
                }
            }
        ),
        types.Tool(
            name="read_file",
            description="Read contents of a text file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to read"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding (default: utf-8)",
                        "default": "utf-8"
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="write_file",
            description="Write content to a file (creates or overwrites)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "Text encoding (default: utf-8)",
                        "default": "utf-8"
                    }
                },
                "required": ["path", "content"]
            }
        ),
        types.Tool(
            name="search_files",
            description="Search for files matching a glob pattern (recursive)",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory to search in"
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern to match (e.g., '*.py', 'test_*.txt')"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 50
                    }
                },
                "required": ["directory", "pattern"]
            }
        ),
        types.Tool(
            name="file_info",
            description="Get detailed information about a file or directory (size, permissions, hash, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file or directory"
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="create_directory",
            description="Create a new directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to create"
                    },
                    "parents": {
                        "type": "boolean",
                        "description": "Create parent directories if needed",
                        "default": True
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="delete_file",
            description="Delete a file (NOT directories, for safety)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to delete"
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="grep_files",
            description="Search for text content within files (like Unix grep)",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory to search in"
                    },
                    "search_term": {
                        "type": "string",
                        "description": "Text to search for"
                    },
                    "file_pattern": {
                        "type": "string",
                        "description": "File pattern to match (default: '*')",
                        "default": "*"
                    },
                    "case_sensitive": {
                        "type": "boolean",
                        "description": "Whether search is case-sensitive",
                        "default": False
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of matches to return",
                        "default": 100
                    }
                },
                "required": ["directory", "search_term"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict[str, Any]
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    
    if name == "list_directory":
        return await list_directory(**arguments)
    elif name == "read_file":
        return await read_file(**arguments)
    elif name == "write_file":
        return await write_file(**arguments)
    elif name == "search_files":
        return await search_files(**arguments)
    elif name == "file_info":
        return await file_info(**arguments)
    elif name == "create_directory":
        return await create_directory(**arguments)
    elif name == "delete_file":
        return await delete_file(**arguments)
    elif name == "grep_files":
        return await grep_files(**arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


# Run server
async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="file-ops-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
