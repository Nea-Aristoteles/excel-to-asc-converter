#!/bin/bash
# Deployment script for Excel to ASC Converter
# Handles pandas compilation issues by using pre-built wheels

set -e  # Exit on any error

echo "🚀 Starting deployment preparation..."

# Check Python version
python_version=$(python3 --version)
echo "📍 Python version: $python_version"

# Upgrade pip first
echo "📦 Upgrading pip..."
pip3 install --upgrade pip

# Try to install with binary wheels only first
echo "🔧 Installing dependencies with binary wheels..."
if pip3 install --only-binary=all --no-compile -r requirements.txt; then
    echo "✅ Successfully installed all dependencies with binary wheels"
else
    echo "⚠️  Binary wheel installation failed, trying lighter requirements..."
    if pip3 install --only-binary=all --no-compile -r requirements-light.txt; then
        echo "✅ Successfully installed with lighter requirements"
    else
        echo "❌ Failed to install dependencies. Please check Python version compatibility."
        exit 1
    fi
fi

# Test the installation
echo "🧪 Testing installation..."
python3 -c "import pandas, flask, openpyxl, gunicorn; print('✅ All modules imported successfully')"

# Test the app startup
echo "🔍 Testing app startup..."
if timeout 10s python3 -c "from app import app; print('✅ App imports successfully')"; then
    echo "✅ App startup test passed"
else
    echo "❌ App startup test failed"
    exit 1
fi

echo "🎉 Deployment preparation completed successfully!"
echo "💡 You can now deploy to Render or run locally with: gunicorn --bind 0.0.0.0:8080 app:app" 