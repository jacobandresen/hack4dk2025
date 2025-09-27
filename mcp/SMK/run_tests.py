#!/usr/bin/env python3
"""
Test runner for SMK MCP Server
Runs both unit tests and integration tests
"""

import asyncio
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print("STDOUT:")
            print(e.stdout)
        if e.stderr:
            print("STDERR:")
            print(e.stderr)
        return False


async def main():
    """Main test runner"""
    print("🧪 SMK MCP Server Test Suite")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    import os
    os.chdir(project_dir)
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not run_command("pip install -r requirements.txt", "Install requirements"):
        print("❌ Failed to install dependencies")
        return False
    
    # Run unit tests
    print("\n🔬 Running unit tests...")
    if not run_command("python -m pytest test_unit.py -v", "Unit tests"):
        print("❌ Unit tests failed")
        return False
    
    # Run integration tests
    print("\n🌐 Running integration tests...")
    if not run_command("python -m pytest test_integration.py -v", "Integration tests"):
        print("❌ Integration tests failed")
        return False
    
    # Run manual integration test
    print("\n🔍 Running manual integration test...")
    try:
        from test_integration import run_integration_tests
        await run_integration_tests()
        print("✅ Manual integration test completed")
    except Exception as e:
        print(f"❌ Manual integration test failed: {e}")
        return False
    
    print("\n🎉 All tests completed successfully!")
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

