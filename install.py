#!/usr/bin/env python
"""
GitHub Clone Crypt - Installation Script
This script automates the setup process for the GitHub Clone Crypt system.
"""

import os
import subprocess
import sys
import platform

def print_step(message):
    """Print a formatted step message."""
    print(f"\n\033[1;34m==>\033[0m \033[1m{message}\033[0m")

def run_command(command, cwd=None):
    """Run a shell command and print its output."""
    print(f"Running: {' '.join(command)}")
    try:
        result = subprocess.run(command, cwd=cwd, check=True, text=True, 
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.stdout and result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError: {e}\033[0m")
        if e.stdout:
            print(e.stdout)
        return False

def check_prerequisites():
    """Check if all prerequisites are installed."""
    print_step("Checking prerequisites")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        print("\033[91mError: Python 3.10+ is required\033[0m")
        return False
    
    print("✓ Python 3.10+ detected")
    
    # Check if MySQL is installed
    try:
        import MySQLdb
        print("✓ MySQL client library detected")
    except ImportError:
        print("\033[91mError: MySQLdb not found. Please install mysqlclient first.\033[0m")
        print("  pip install mysqlclient")
        return False
    
    # Check Node.js and npm (for frontend)
    try:
        node_version = subprocess.run(['node', '--version'], check=True, capture_output=True, text=True).stdout.strip()
        npm_version = subprocess.run(['npm', '--version'], check=True, capture_output=True, text=True).stdout.strip()
        print(f"✓ Node.js {node_version} and npm {npm_version} detected")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\033[93mWarning: Node.js and npm are required for the frontend but were not detected\033[0m")
        print("You can still set up the backend and CLI tool.")
    
    return True

def setup_database():
    """Set up the MySQL database."""
    print_step("Setting up database")
    
    # Create database
    if not run_command([sys.executable, 'create_db.py']):
        return False
    
    # Apply migrations
    return run_command([sys.executable, 'manage.py', 'migrate'], cwd='crpt_backend')

def setup_backend():
    """Set up the Django backend."""
    print_step("Setting up backend")
    
    # Install Python requirements
    if not run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']):
        return False
    
    print("Backend setup complete. You can start the server with:")
    print("  cd crpt_backend && python manage.py runserver")
    return True

def setup_frontend():
    """Set up the React frontend."""
    print_step("Setting up frontend")
    
    frontend_dir = os.path.join('frontend', 'crpt-frontend')
    
    # Check if npm is available
    try:
        subprocess.run(['npm', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\033[93mWarning: npm not found. Skipping frontend setup.\033[0m")
        return True
    
    # Install npm dependencies
    if not run_command(['npm', 'install'], cwd=frontend_dir):
        return False
    
    print("Frontend setup complete. You can start the development server with:")
    print(f"  cd {frontend_dir} && npm start")
    return True

def setup_cli():
    """Set up the CLI tool."""
    print_step("Setting up CLI tool")
    
    # Install in development mode
    if not run_command([sys.executable, '-m', 'pip', 'install', '-e', '.']):
        return False
    
    print("CLI tool setup complete. You can verify it with:")
    print("  crpt --help")
    return True

def main():
    """Main installation function."""
    print("\033[1;32m===== GitHub Clone Crypt - Installation =====\033[0m")
    
    if not check_prerequisites():
        sys.exit(1)
    
    if not setup_database():
        print("\033[91mDatabase setup failed. Exiting.\033[0m")
        sys.exit(1)
    
    if not setup_backend():
        print("\033[91mBackend setup failed. Exiting.\033[0m")
        sys.exit(1)
    
    setup_frontend()  # Frontend setup is optional
    
    if not setup_cli():
        print("\033[91mCLI tool setup failed. Exiting.\033[0m")
        sys.exit(1)
    
    print("\n\033[1;32m===== Installation Complete! =====\033[0m")
    print("""
To start using GitHub Clone Crypt:

1. Start the Django backend:
   cd crpt_backend && python manage.py runserver

2. Start the React frontend:
   cd frontend/crpt-frontend && npm start

3. Use the CLI tool to create and manage repositories:
   crpt init
   crpt add <file>
   crpt commit -m "Commit message"
   crpt push
   crpt pull
    """)

if __name__ == "__main__":
    main()