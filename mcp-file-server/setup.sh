#!/bin/bash
# Setup script for File Operations MCP Server

set -e

echo "=================================="
echo "File Operations MCP Server Setup"
echo "=================================="
echo

# Get the absolute path to the server
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_PATH="$SCRIPT_DIR/server.py"

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo

# Make server executable
chmod +x server.py
chmod +x test_server.py
echo "✅ Made scripts executable"
echo

# Run tests
echo "Running tests..."
python3 test_server.py
echo

# Print configuration instructions
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo
echo "Server location: $SERVER_PATH"
echo
echo "To use with Claude Desktop, add this to your config file:"
echo
echo "macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
echo "Linux: ~/.config/Claude/claude_desktop_config.json"
echo
echo "{"
echo "  \"mcpServers\": {"
echo "    \"file-ops\": {"
echo "      \"command\": \"python3\","
echo "      \"args\": [\"$SERVER_PATH\"]"
echo "    }"
echo "  }"
echo "}"
echo
echo "Then restart Claude Desktop."
echo
echo "To test the server manually:"
echo "  source venv/bin/activate"
echo "  python3 test_server.py"
echo
echo "To use MCP Inspector (for debugging):"
echo "  npx @anthropics/mcp-inspector python3 $SERVER_PATH"
echo
