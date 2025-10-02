#!/bin/bash
# MCP Local LLM - Development Setup Script
# Optimized for small coder model training on Apple M1 Max

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_status "🚀 Setting up MCP Local LLM for training development..."
echo ""

# ============================================================================
# Check Prerequisites
# ============================================================================
print_status "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.11 or later."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    print_error "Python 3.11+ required. Current: $PYTHON_VERSION"
    exit 1
fi

print_success "Python $PYTHON_VERSION detected"

# Check pip
if ! python3 -m pip --version &> /dev/null; then
    print_error "pip is not installed. Please install pip."
    exit 1
fi

print_success "pip detected"

# ============================================================================
# Create Virtual Environment
# ============================================================================
print_status "Creating virtual environment..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists (skipping)"
fi

# Activate virtual environment
source .venv/bin/activate
print_success "Virtual environment activated"

# ============================================================================
# Install Dependencies
# ============================================================================
print_status "Installing Python dependencies..."

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

print_success "Dependencies installed"

# ============================================================================
# Create Development Directories
# ============================================================================
print_status "Creating development directories..."

mkdir -p data logs policy docs/examples tests/fixtures
print_success "Directories created: data/, logs/, policy/, docs/examples/, tests/fixtures/"

# ============================================================================
# Setup Environment Configuration
# ============================================================================
print_status "Setting up environment configuration..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Created .env from .env.example"
        print_warning "⚠️  Please review and customize .env for your environment"
    else
        print_warning ".env.example not found (skipping .env creation)"
    fi
else
    print_warning ".env already exists (skipping)"
fi

# Copy example config if needed
if [ ! -f "config.yaml" ] && [ -f "config.example.yaml" ]; then
    cp config.example.yaml config.yaml
    print_success "Created config.yaml from config.example.yaml"
fi

# ============================================================================
# Check Docker (Optional)
# ============================================================================
print_status "Checking Docker availability..."

if command -v docker &> /dev/null; then
    print_success "Docker detected"
    
    # Check if Docker daemon is running
    if docker info &> /dev/null; then
        print_success "Docker daemon is running"
        
        # Check if Qdrant container exists
        if docker ps -a --format '{{.Names}}' | grep -q "mcp-qdrant-training\|qdrant"; then
            print_warning "Qdrant container already exists"
            print_status "To restart: docker-compose restart qdrant"
        else
            print_status "To start Qdrant: docker-compose up -d qdrant"
        fi
    else
        print_warning "Docker daemon not running. Start Docker Desktop to use Qdrant."
    fi
else
    print_warning "Docker not found (optional). You can install Docker later for local Qdrant."
fi

# ============================================================================
# Create Example Policy Files (if needed)
# ============================================================================
if [ ! -f "policy/01-principles.md" ]; then
    print_status "Creating example policy files..."
    
    cat > policy/01-principles.md << 'EOF'
# Core Principles

## [P-001] Code Quality
All code must follow project standards: black formatting, ruff linting, mypy type checking.

## [P-002] Test Coverage
Minimum 85% line coverage and 75% branch coverage required for all modules.

## [P-003] Documentation
All public APIs must be documented with clear docstrings and type hints.
EOF

    print_success "Example policy files created"
fi

# ============================================================================
# Display Setup Summary
# ============================================================================
echo ""
print_success "🎉 Development setup completed!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Environment Information:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  • Python Version:    $PYTHON_VERSION"
echo "  • Virtual Env:       .venv (activated)"
echo "  • Configuration:     .env, config.yaml"
echo "  • Data Directory:    ./data/"
echo "  • Logs Directory:    ./logs/"
echo "  • Policy Directory:  ./policy/"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Development Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  • Activate venv:     source .venv/bin/activate"
echo "  • Validate setup:    make validate-env"
echo "  • Format code:       make fmt"
echo "  • Run tests:         make test"
echo "  • Quality gates:     make gates"
echo "  • Build package:     make build"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐳 Docker Commands (Optional):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  • Start Qdrant:      docker-compose up -d qdrant"
echo "  • Stop Qdrant:       docker-compose stop qdrant"
echo "  • View logs:         docker-compose logs -f qdrant"
echo "  • Qdrant Dashboard:  http://localhost:6333/dashboard"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  1. Review and customize .env for your setup"
echo "  2. Start Qdrant: docker-compose up -d qdrant"
echo "  3. Validate environment: make validate-env"
echo "  4. Run tests: make test"
echo "  5. Start developing! 🚀"
echo ""

print_success "Happy coding! 🎉"
