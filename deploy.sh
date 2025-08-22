#!/bin/bash

# Abide: Christian AI Companion - Deployment Script
# This script helps deploy the application to various platforms

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_commands=()
    
    if ! command_exists docker; then
        missing_commands+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_commands+=("docker-compose")
    fi
    
    if ! command_exists python3; then
        missing_commands+=("python3")
    fi
    
    if ! command_exists pip; then
        missing_commands+=("pip")
    fi
    
    if ! command_exists node; then
        missing_commands+=("node")
    fi
    
    if ! command_exists npm; then
        missing_commands+=("npm")
    fi
    
    if [ ${#missing_commands[@]} -ne 0 ]; then
        print_error "Missing required commands: ${missing_commands[*]}"
        print_status "Please install the missing commands and try again."
        exit 1
    fi
    
    print_success "All prerequisites are installed!"
}

# Function to setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    # Create backend environment file if it doesn't exist
    if [ ! -f "backend/.env" ]; then
        if [ -f "backend/env.example" ]; then
            cp backend/env.example backend/.env
            print_warning "Created backend/.env from example. Please edit it with your actual values."
        else
            print_error "Backend environment example file not found!"
            exit 1
        fi
    fi
    
    # Create frontend environment file if it doesn't exist
    if [ ! -f "frontend/.env.local" ]; then
        if [ -f "frontend/env.example" ]; then
            cp frontend/env.example frontend/.env.local
            print_warning "Created frontend/.env.local from example. Please edit it with your actual values."
        else
            print_error "Frontend environment example file not found!"
            exit 1
        fi
    fi
    
    print_success "Environment files created!"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Install backend dependencies
    print_status "Installing Python dependencies..."
    cd backend
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    
    # Install frontend dependencies
    print_status "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
    
    print_success "Dependencies installed!"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    print_status "Running backend tests..."
    cd backend
    source venv/bin/activate
    python test_main.py
    cd ..
    
    print_success "Tests completed!"
}

# Function to start development environment
start_dev() {
    print_status "Starting development environment..."
    
    # Start with Docker Compose
    if [ "$1" = "docker" ]; then
        print_status "Starting with Docker Compose..."
        docker-compose up -d
        
        print_success "Development environment started!"
        print_status "Backend: http://localhost:8000"
        print_status "Frontend: http://localhost:3000"
        print_status "PostgreSQL: localhost:5432"
        print_status "Redis: localhost:6379"
        
        print_status "To view logs: docker-compose logs -f"
        print_status "To stop: docker-compose down"
        
    else
        print_status "Starting services individually..."
        
        # Start PostgreSQL and Redis with Docker
        print_status "Starting PostgreSQL and Redis..."
        docker-compose up -d postgres redis
        
        # Wait for services to be ready
        print_status "Waiting for services to be ready..."
        sleep 10
        
        # Start backend
        print_status "Starting backend..."
        cd backend
        source venv/bin/activate
        uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
        BACKEND_PID=$!
        cd ..
        
        # Start frontend
        print_status "Starting frontend..."
        cd frontend
        npm run dev &
        FRONTEND_PID=$!
        cd ..
        
        print_success "Development environment started!"
        print_status "Backend: http://localhost:8000 (PID: $BACKEND_PID)"
        print_status "Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
        print_status "PostgreSQL: localhost:5432"
        print_status "Redis: localhost:6379"
        
        print_status "To stop services, kill PIDs: $BACKEND_PID $FRONTEND_PID"
        print_status "Or use: pkill -f 'uvicorn main:app' && pkill -f 'npm run dev'"
    fi
}

# Function to build production images
build_production() {
    print_status "Building production Docker images..."
    
    docker-compose -f docker-compose.yml build
    
    print_success "Production images built!"
}

# Function to deploy to production
deploy_production() {
    print_status "Deploying to production..."
    
    # This is a placeholder for production deployment
    # You would typically integrate with your deployment platform here
    
    print_warning "Production deployment not configured."
    print_status "Please configure your deployment platform (Render, Fly.io, etc.)"
    print_status "or modify this script for your specific needs."
}

# Function to show help
show_help() {
    echo "Abide: Christian AI Companion - Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  check       Check prerequisites"
    echo "  setup       Setup environment files"
    echo "  install     Install dependencies"
    echo "  test        Run tests"
    echo "  dev         Start development environment"
    echo "  dev:docker  Start development environment with Docker"
    echo "  build       Build production Docker images"
    echo "  deploy      Deploy to production (placeholder)"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 check              # Check if all required tools are installed"
    echo "  $0 setup              # Create environment files"
    echo "  $0 install            # Install all dependencies"
    echo "  $0 test               # Run tests"
    echo "  $0 dev                # Start development environment"
    echo "  $0 dev:docker         # Start development environment with Docker"
    echo "  $0 build              # Build production images"
}

# Main script logic
case "${1:-help}" in
    "check")
        check_prerequisites
        ;;
    "setup")
        setup_environment
        ;;
    "install")
        install_dependencies
        ;;
    "test")
        run_tests
        ;;
    "dev")
        start_dev
        ;;
    "dev:docker")
        start_dev docker
        ;;
    "build")
        build_production
        ;;
    "deploy")
        deploy_production
        ;;
    "help"|*)
        show_help
        ;;
esac
