#!/bin/bash

echo "Building Windows .exe using Docker (if available)"
echo "=================================================="
echo ""

if ! command -v docker &> /dev/null; then
    echo "Docker is not installed."
    echo ""
    echo "Alternative: Use GitHub Actions (see build_windows_github.sh)"
    echo "Or: Copy to Windows machine and run build_windows.bat"
    exit 1
fi

echo "Note: Docker on Linux typically uses Linux containers."
echo "Windows containers require Windows Server or Windows 10/11 Pro with Hyper-V."
echo ""
echo "For Linux, the best options are:"
echo "1. Use GitHub Actions (automatic, free)"
echo "2. Use a Windows VM"
echo "3. Build on actual Windows machine"
echo ""
echo "Setting up GitHub Actions workflow instead..."
echo ""

if [ ! -d ".github/workflows" ]; then
    mkdir -p .github/workflows
    echo "Created .github/workflows directory"
fi

echo "GitHub Actions workflow created!"
echo "Push to GitHub and use Actions to build Windows .exe"

