#!/usr/bin/env python3
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("🚀 Starting Excel to ASC Converter Web Server...")
    print("📡 Server will be available at: http://localhost:8080")
    print("📋 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8080)
    
except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    print("💡 Make sure you have installed all dependencies:")
    print("   pip3 install --user --break-system-packages -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting server: {e}")
    sys.exit(1) 