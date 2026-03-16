#!/usr/bin/env python3
"""
Test script for the File Operations MCP Server

This script demonstrates how the tools work without needing Claude.
"""

import asyncio
import sys
from pathlib import Path

# Import the server tools directly
sys.path.insert(0, str(Path(__file__).parent))
from server import (
    list_directory,
    read_file,
    write_file,
    search_files,
    file_info,
    create_directory,
    delete_file,
    grep_files
)


def print_result(result):
    """Print the text content from tool result."""
    if result and len(result) > 0:
        print(result[0].text)
    else:
        print("(no result)")


async def run_tests():
    """Run a series of tests to demonstrate the server capabilities."""
    
    print("=" * 70)
    print("File Operations MCP Server - Test Suite")
    print("=" * 70)
    
    # Create test directory
    print("\n📁 TEST 1: Create Directory")
    print("-" * 70)
    result = await create_directory("test_output")
    print_result(result)
    
    # Write a test file
    print("\n📝 TEST 2: Write File")
    print("-" * 70)
    test_content = """# Test File
This is a test file created by the MCP server.

TODO: Add more content
Features:
- Easy file operations
- Search capabilities
- Safe deletion"""
    
    result = await write_file("test_output/test.txt", test_content)
    print_result(result)
    
    # Read the file back
    print("\n📖 TEST 3: Read File")
    print("-" * 70)
    result = await read_file("test_output/test.txt")
    print_result(result)
    
    # Get file info
    print("\n📊 TEST 4: File Info")
    print("-" * 70)
    result = await file_info("test_output/test.txt")
    print_result(result)
    
    # List directory
    print("\n📂 TEST 5: List Directory")
    print("-" * 70)
    result = await list_directory("test_output")
    print_result(result)
    
    # Write another file for search tests
    await write_file("test_output/config.json", '{"name": "test", "version": "1.0"}')
    await write_file("test_output/notes.md", "# Notes\n\nTODO: Review this file\n\nSome notes here.")
    
    # Search for files
    print("\n🔍 TEST 6: Search Files (*.txt)")
    print("-" * 70)
    result = await search_files("test_output", "*.txt")
    print_result(result)
    
    # Grep for content
    print("\n🔎 TEST 7: Grep Files (search for 'TODO')")
    print("-" * 70)
    result = await grep_files("test_output", "TODO", "*")
    print_result(result)
    
    # Clean up one file
    print("\n🗑️  TEST 8: Delete File")
    print("-" * 70)
    result = await delete_file("test_output/test.txt")
    print_result(result)
    
    # List directory again
    print("\n📂 TEST 9: List Directory After Deletion")
    print("-" * 70)
    result = await list_directory("test_output")
    print_result(result)
    
    print("\n" + "=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)
    print("\nTest files remain in 'test_output/' directory for inspection.")
    print("You can delete it manually when done: rm -rf test_output")


if __name__ == "__main__":
    asyncio.run(run_tests())
