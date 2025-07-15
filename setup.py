#!/usr/bin/env python3
"""
Road Hazard Detection & Mapping System Setup Script
This script helps set up the development environment and run the application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, 
                              capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if required software is installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    if not run_command("python --version"):
        print("❌ Python 3.8+ is required")
        return False
    
    # Check Node.js
    if not run_command("node --version"):
        print("❌ Node.js 16+ is required")
        return False
    
    # Check PostgreSQL
    if not run_command("psql --version"):
        print("❌ PostgreSQL with PostGIS is required")
        return False
    
    print("✅ All prerequisites found!")
    return True

def setup_backend():
    """Set up the backend Flask application"""
    print("\n🔧 Setting up backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Create virtual environment
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        if not run_command("python -m venv venv", cwd=backend_dir):
            return False
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        pip_path = venv_path / "Scripts" / "pip"
        python_path = venv_path / "Scripts" / "python"
    else:  # Unix/Linux/macOS
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    if not run_command(f"{pip_path} install -r requirements.txt", cwd=backend_dir):
        return False
    
    # Create environment file if it doesn't exist
    env_file = backend_dir / ".env"
    if not env_file.exists():
        env_content = """DATABASE_URL=postgresql://postgres:password@localhost:5432/road_hazards
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
MAPBOX_ACCESS_TOKEN=your_mapbox_token_here
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file (please update with your credentials)")
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Set up the frontend React application"""
    print("\n🔧 Setting up frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install Node.js dependencies
    if not run_command("npm install", cwd=frontend_dir):
        return False
    
    # Create environment file if it doesn't exist
    env_file = frontend_dir / ".env"
    if not env_file.exists():
        env_content = """REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file (please update with your Mapbox token)")
    
    print("✅ Frontend setup complete!")
    return True

def setup_database():
    """Set up the PostgreSQL database"""
    print("\n🗄️ Setting up database...")
    
    # Create database (this might fail if already exists, which is fine)
    run_command("createdb road_hazards")
    
    # Enable PostGIS extension
    run_command("psql -d road_hazards -c 'CREATE EXTENSION IF NOT EXISTS postgis;'")
    
    print("✅ Database setup complete!")
    return True

def generate_dummy_data():
    """Generate dummy data for testing"""
    print("\n📊 Generating dummy data...")
    
    backend_dir = Path("backend")
    data_script = backend_dir / "data" / "dummy_data_generator.py"
    
    if not data_script.exists():
        print("❌ Dummy data generator not found")
        return False
    
    # Run the dummy data generator
    if os.name == 'nt':  # Windows
        python_path = backend_dir / "venv" / "Scripts" / "python"
    else:  # Unix/Linux/macOS
        python_path = backend_dir / "venv" / "bin" / "python"
    
    if not run_command(f"{python_path} {data_script}", cwd=backend_dir):
        return False
    
    print("✅ Dummy data generation complete!")
    return True

def start_servers():
    """Start both backend and frontend servers"""
    print("\n🚀 Starting servers...")
    
    # Instructions for manual start since we can't easily manage both processes
    print("""
To start the application:

1. Start the backend server:
   cd backend
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   python app.py

2. In a new terminal, start the frontend server:
   cd frontend
   npm start

3. Open your browser and navigate to:
   http://localhost:3000

The backend API will be available at:
   http://localhost:5000
""")

def main():
    """Main setup function"""
    print("🛣️  Road Hazard Detection & Mapping System Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Setup components
    success = True
    success &= setup_backend()
    success &= setup_frontend()
    success &= setup_database()
    success &= generate_dummy_data()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        start_servers()
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 