#!/usr/bin/env python3
"""
Script to build and upload Python package to Nexus repository.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ {command}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return False


def clean_build_artifacts():
    """Clean previous build artifacts."""
    artifacts = ['build', 'dist', '*.egg-info']
    for artifact in artifacts:
        for path in Path('.').glob(artifact):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
            else:
                path.unlink()
                print(f"Removed file: {path}")


def build_package():
    """Build the Python package."""
    print("Building package...")
    return run_command("python -m build")


def upload_to_nexus():
    """Upload package to Nexus repository."""
    print("Uploading to Nexus repository...")
    
    # Check if .pypirc exists
    pypirc_path = Path(".pypirc")
    if not pypirc_path.exists():
        print("Error: .pypirc file not found. Please configure your Nexus credentials.")
        return False
    
    # Upload using twine
    return run_command(f"twine upload --config-file .pypirc --repository nexus dist/*")


def main():
    """Main function to orchestrate the build and upload process."""
    print("Starting package build and upload process...")
    
    # Check if required tools are installed
    required_tools = ['python', 'twine']
    for tool in required_tools:
        if not shutil.which(tool):
            print(f"Error: {tool} is not installed or not in PATH")
            sys.exit(1)
    
    # Clean previous builds
    clean_build_artifacts()
    
    # Build the package
    if not build_package():
        print("Build failed!")
        sys.exit(1)
    
    # Upload to Nexus
    if not upload_to_nexus():
        print("Upload failed!")
        sys.exit(1)
    
    print("✓ Package successfully built and uploaded to Nexus!")


if __name__ == "__main__":
    main()
