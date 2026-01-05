#!/bin/bash
# Perfect Web Clone - Setup Script
# Installs all dependencies needed for the skill

set -e

echo "=================================="
echo "Perfect Web Clone - Setup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "ERROR: pip is required but not installed."
    exit 1
fi

PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "Installing Python dependencies..."
$PIP_CMD install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "Installing Playwright browsers..."
python3 -m playwright install chromium

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "You can now use the Perfect Web Clone skill in Claude Code."
echo ""
echo "Test the installation:"
echo "  python3 $SCRIPT_DIR/extract_page.py https://example.com -o test.json"
echo ""
