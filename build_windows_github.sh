#!/bin/bash

echo "=========================================="
echo "Build Windows .exe using GitHub Actions"
echo "=========================================="
echo ""

if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for Windows build"
fi

echo "This script will:"
echo "1. Push code to GitHub (if not already)"
echo "2. Trigger GitHub Actions to build Windows .exe"
echo "3. Download the built .exe file"
echo ""
read -p "Do you have a GitHub repository? (y/n): " has_repo

if [ "$has_repo" != "y" ]; then
    echo ""
    echo "To build Windows .exe automatically:"
    echo "1. Create a GitHub repository"
    echo "2. Push this code to GitHub"
    echo "3. GitHub Actions will automatically build the .exe"
    echo ""
    echo "Or use the manual method:"
    echo "  - Copy project to Windows machine"
    echo "  - Run: build_windows.bat"
    exit 0
fi

echo ""
echo "GitHub Actions workflow is ready at: .github/workflows/build-windows.yml"
echo ""
echo "To build:"
echo "1. Push code to GitHub"
echo "2. Go to Actions tab in GitHub"
echo "3. Run the 'Build Windows Executable' workflow"
echo "4. Download the artifact"
echo ""

