#!/usr/bin/env python3
"""
Start All Script
Launches both backend and frontend servers simultaneously
"""

import subprocess
import sys
import os
from pathlib import Path

def start_backend():
    """Start the backend server"""
    backend_dir = Path(__file__).parent / "backend"
    print("Starting backend server...")
    print(f"Backend directory: {backend_dir}")
    
    backend_process = subprocess.Popen(
        [".venv/bin/uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return backend_process

def start_frontend():
    """Start the frontend server"""
    frontend_dir = Path(__file__).parent / "frontend"
    print("Starting frontend server...")
    print(f"Frontend directory: {frontend_dir}")
    
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return frontend_process

def main():
    """Main function to start both servers"""
    print("=" * 50)
    print("Starting MJ CRM System")
    print("=" * 50)
    
    # Check if directories exist
    backend_dir = Path(__file__).parent / "backend"
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not backend_dir.exists():
        print(f"Error: Backend directory not found: {backend_dir}")
        sys.exit(1)
    
    if not frontend_dir.exists():
        print(f"Error: Frontend directory not found: {frontend_dir}")
        sys.exit(1)
    
    # Start servers
    try:
        backend_process = start_backend()
        frontend_process = start_frontend()
        
        print("\n" + "=" * 50)
        print("Servers started successfully!")
        print("=" * 50)
        print("Backend: http://localhost:8000")
        print("Backend API Docs: http://localhost:8000/docs")
        print("Frontend: Check terminal for URL (usually http://localhost:5173)")
        print("=" * 50)
        print("\nPress Ctrl+C to stop both servers")
        
        # Wait for processes
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped.")
    except Exception as e:
        print(f"Error starting servers: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
