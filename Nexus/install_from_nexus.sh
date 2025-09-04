#!/bin/bash

# Script to install packages from Nexus repository
# Usage: ./install_from_nexus.sh [package-name]

NEXUS_URL="http://admin:Aa123456@34.233.125.126:8081/repository/my-int-pypi/simple/"
PACKAGE_NAME=${1:-"nexus-example-package"}

echo "🔍 Installing package: $PACKAGE_NAME"
echo "📦 From Nexus repository: $NEXUS_URL"

# Install the package from Nexus
pip3 install --extra-index-url "$NEXUS_URL" --trusted-host 34.233.125.126 "$PACKAGE_NAME"

if [ $? -eq 0 ]; then
    echo "✅ Package $PACKAGE_NAME installed successfully!"
else
    echo "❌ Failed to install package $PACKAGE_NAME"
    exit 1
fi
