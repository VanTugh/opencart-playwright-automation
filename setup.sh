#!/bin/bash

# OpenCart Automation Testing Framework - Quick Setup Script
# This script sets up the environment and installs all dependencies

echo "=========================================="
echo "OpenCart Automation Testing Framework"
echo "Quick Setup Script"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python version: $(python3 --version)"

# Create virtual environment (optional but recommended)
echo ""
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate 2>/dev/null || . .venv/Scripts/activate 2>/dev/null
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip -q
echo "✓ Pip upgraded"

# Install requirements
echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt -q
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers (this may take a few minutes)..."
playwright install chromium -q
if [ $? -eq 0 ]; then
    echo "✓ Playwright browsers installed"
else
    echo "⚠️  Warning: Playwright browser installation may need manual setup"
fi

# Create necessary directories
echo ""
echo "Setting up project directories..."
mkdir -p logs
mkdir -p reports
mkdir -p failures
echo "✓ Directories created:"
echo "  - logs/       (for test execution logs)"
echo "  - reports/    (for HTML test reports)"
echo "  - failures/   (for failure screenshots)"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file from .env.example"
    echo "  Edit .env to customize configuration"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file if needed (optional)"
echo "2. Run tests: python run_tests.py"
echo "3. Or use pytest directly: pytest main.py -v"
echo ""
echo "For more information, see README.md"
echo ""

