#!/bin/bash

# Build and Upload Script for Nexus Repository
# This script builds the Python package and uploads it to the specified Nexus repository

set -e  # Exit on any error

echo "🚀 Starting build and upload process..."

# Check if required tools are installed
command -v python3 >/dev/null 2>&1 || { echo "❌ Python is required but not installed. Aborting." >&2; exit 1; }
command -v pip >/dev/null 2>&1 || { echo "❌ pip is required but not installed. Aborting." >&2; exit 1; }

# Install required dependencies if not already installed
echo "📦 Installing build dependencies..."
pip install --upgrade build twine

# Clean previous build artifacts
echo "🧹 Cleaning previous build artifacts..."
rm -rf build/ dist/ *.egg-info/

# Build the package
echo "🔨 Building package..."
python3 -m build

# Check if dist directory was created and contains files
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    echo "❌ Build failed - no distribution files created"
    exit 1
fi

echo "✅ Package built successfully!"
echo "📁 Distribution files created:"
ls -la dist/

# Upload to Nexus (requires credentials to be configured in .pypirc)
echo "📤 Uploading to Nexus repository..."
if [ -f ".pypirc" ]; then
    twine upload --config-file .pypirc --repository nexus dist/*
    echo "✅ Package uploaded successfully to Nexus!"
else
    echo "⚠️  .pypirc not found. Please configure your Nexus credentials first."
    echo "📝 Update the .pypirc file with your actual Nexus username and password"
    echo "🔧 Then run: twine upload --config-file .pypirc --repository nexus dist/*"
fi

echo "🎉 Process completed!"
