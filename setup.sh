#!/bin/bash

# AI-mVISE Repository Analyzer Setup Script
# Modern Glassmorphism UI Edition
echo "🚀 Setting up AI-mVISE Repository Analyzer with Modern UI..."
echo "======================================================================"

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}
╔═══════════════════════════════════════════════════════════════╗
║                   🤖 AI-mVISE Setup                         ║
║              Modern Glassmorphism UI Edition                  ║
╚═══════════════════════════════════════════════════════════════╝${NC}"
}

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# System Requirements Check
print_header

print_status "Checking system requirements..."

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
    
    # Check if version is >= 18
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$NODE_MAJOR" -lt 18 ]; then
        print_error "Node.js version 18 or higher is required. Please upgrade."
        exit 1
    fi
else
    print_error "Node.js is not installed. Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check npm
if command_exists npm; then
    NPM_VERSION=$(npm --version)
    print_success "npm found: $NPM_VERSION"
else
    print_error "npm is not installed. Please install npm."
    exit 1
fi

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
elif command_exists python; then
    PYTHON_VERSION=$(python --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python is not installed. Please install Python 3.8+ from https://python.org/"
    exit 1
fi

# Check pip
if command_exists pip3; then
    PIP_VERSION=$(pip3 --version)
    print_success "pip found: $PIP_VERSION"
    PIP_CMD="pip3"
elif command_exists pip; then
    PIP_VERSION=$(pip --version)
    print_success "pip found: $PIP_VERSION"
    PIP_CMD="pip"
else
    print_error "pip is not installed. Please install pip."
    exit 1
fi

echo ""
print_status "🔧 Installing dependencies..."

# Install root dependencies
print_status "Installing root project dependencies..."
if npm install; then
    print_success "Root dependencies installed successfully"
else
    print_error "Failed to install root dependencies"
    exit 1
fi

# Setup Frontend
echo ""
print_status "📱 Setting up Frontend (Modern React UI)..."
cd frontend

# Install frontend dependencies (including new modern UI packages)
print_status "Installing frontend dependencies with modern UI packages..."
if npm install; then
    print_success "Frontend dependencies installed successfully"
else
    print_error "Failed to install frontend dependencies"
    exit 1
fi

# Create frontend .env file
print_status "Creating frontend environment configuration..."
cat > .env.local << EOL
# Frontend Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=AI-mVISE Repository Analyzer
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DARK_MODE=true
NEXT_PUBLIC_DEFAULT_THEME=dark
EOL
print_success "Frontend .env.local created"

cd ..

# Setup Backend
echo ""
print_status "🔧 Setting up Backend (FastAPI)..."
cd backend

# Create virtual environment
print_status "Creating Python virtual environment..."
if python3 -m venv venv 2>/dev/null || python -m venv venv; then
    print_success "Virtual environment created"
else
    print_error "Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment and install dependencies
print_status "Installing backend dependencies..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/macOS
    source venv/bin/activate
fi

# Upgrade pip first
$PIP_CMD install --upgrade pip

# Install dependencies
if $PIP_CMD install -r requirements.txt; then
    print_success "Backend dependencies installed successfully"
else
    print_error "Failed to install backend dependencies"
    exit 1
fi

# Create backend .env file
print_status "Creating backend environment configuration..."
cat > .env << EOL
# Database Configuration
DATABASE_URL=sqlite:///./ai_mvise.db
# For PostgreSQL (uncomment and configure):
# DATABASE_URL=postgresql://username:password@localhost/ai_mvise

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0

# GitHub API Configuration
GITHUB_TOKEN=your_github_token_here

# AI Service Configuration
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here

# Application Settings
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Analysis Settings
MAX_ANALYSIS_TIME=3600
MAX_REPOSITORY_SIZE=1000000000
ENABLE_CACHING=true

# File Storage
UPLOAD_DIR=./uploads
REPORTS_DIR=./reports
LOG_LEVEL=INFO

# Security Settings
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Analysis Thresholds
QUALITY_THRESHOLD_LOW=2.0
QUALITY_THRESHOLD_MEDIUM=4.0
SECURITY_THRESHOLD_HIGH=0.8
COMPLEXITY_THRESHOLD_HIGH=10
EOL
print_success "Backend .env created with secure random secret key"

# Initialize database
print_status "Initializing database..."
if python -c "
from app.core.database import init_db
try:
    init_db()
    print('Database initialized successfully')
except Exception as e:
    print(f'Database initialization failed: {e}')
    exit(1)
"; then
    print_success "Database initialized"
else
    print_warning "Database initialization had issues (this is normal for first run)"
fi

cd ..

# Final success message
echo ""
echo -e "${GREEN}
╔═══════════════════════════════════════════════════════════════╗
║                  🎉 SETUP COMPLETE! 🎉                      ║
║                                                               ║
║  AI-mVISE Repository Analyzer with Modern UI is ready!       ║
╚═══════════════════════════════════════════════════════════════╝${NC}"

echo ""
print_success "🚀 Your AI-mVISE installation is complete!"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo -e "  ${YELLOW}1.${NC} Configure your API keys in ${BLUE}backend/.env${NC}"
echo -e "  ${YELLOW}2.${NC} Start the development servers:"
echo -e "     ${GREEN}npm run dev${NC}     (starts both frontend and backend)"
echo -e "  ${YELLOW}3.${NC} Or start them separately:"
echo -e "     ${GREEN}npm run dev:backend${NC}   (FastAPI on http://localhost:8000)"
echo -e "     ${GREEN}npm run dev:frontend${NC}  (Next.js on http://localhost:3000)"
echo ""
echo -e "${PURPLE}Features included:${NC}"
echo -e "  ✨ Modern Glassmorphism UI with dark theme"
echo -e "  🤖 AI-powered repository analysis" 
echo -e "  🔍 Comprehensive code quality metrics"
echo -e "  🛡️  Advanced security scanning"
echo -e "  📊 Interactive dashboards and reports"
echo -e "  🎨 Beautiful animations and transitions"
echo ""
echo -e "${BLUE}Documentation:${NC} Check the README.md for detailed usage instructions"
echo -e "${BLUE}Issues?${NC} Visit our GitHub repository for support"
echo ""
print_success "Happy analyzing! 🎯" 