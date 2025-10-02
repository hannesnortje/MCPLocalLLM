#!/usr/bin/env python3
"""
MCP Local LLM - Environment Validation Script
Validates development environment for small coder model training
"""

import os
import sys
from pathlib import Path
from typing import Any


# Colors for terminal output
class Colors:
    """Terminal color codes."""

    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def print_status(message: str) -> None:
    """Print info status message."""
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")


def print_success(message: str) -> None:
    """Print success message."""
    print(f"{Colors.GREEN}[✓]{Colors.NC} {message}")


def print_warning(message: str) -> None:
    """Print warning message."""
    print(f"{Colors.YELLOW}[⚠]{Colors.NC} {message}")


def print_error(message: str) -> None:
    """Print error message."""
    print(f"{Colors.RED}[✗]{Colors.NC} {message}")


def check_python_version() -> tuple[bool, str]:
    """Check if Python version is 3.11+."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 11:
        return True, f"Python {version_str}"
    return False, f"Python {version_str} (3.11+ required)"


def check_directory_exists(path: Path, name: str) -> tuple[bool, str]:
    """Check if directory exists."""
    if path.exists() and path.is_dir():
        return True, f"Directory '{name}' exists"
    return False, f"Directory '{name}' not found (run setup-dev.sh)"


def check_file_exists(path: Path, name: str) -> tuple[bool, str]:
    """Check if file exists."""
    if path.exists() and path.is_file():
        return True, f"File '{name}' exists"
    return False, f"File '{name}' not found"


def check_env_file() -> tuple[bool, str]:
    """Check if .env file exists and is properly configured."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")

    if not env_path.exists():
        if env_example_path.exists():
            return False, ".env not found (copy from .env.example)"
        return False, ".env and .env.example not found"

    # Check if .env is not empty
    if env_path.stat().st_size == 0:
        return False, ".env is empty (copy from .env.example)"

    return True, ".env file exists and configured"


def check_virtual_env() -> tuple[bool, str]:
    """Check if virtual environment exists and is activated."""
    venv_path = Path(".venv")

    # Check if .venv exists
    if not venv_path.exists():
        return False, "Virtual environment not found (run setup-dev.sh)"

    # Check if currently activated
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        return True, "Virtual environment exists and activated"

    return True, "Virtual environment exists (not activated: source .venv/bin/activate)"


def check_docker() -> tuple[bool, str]:
    """Check if Docker is available (optional)."""
    import shutil
    import subprocess

    # Check if docker command exists
    if not shutil.which("docker"):
        return False, "Docker not found (optional - install for local Qdrant)"

    # Check if Docker daemon is running
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            return True, "Docker available and running"
        return False, "Docker installed but daemon not running"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "Docker check failed (optional)"


def check_dependencies() -> tuple[bool, str]:
    """Check if key dependencies are installed."""
    try:
        # Check core dependencies
        import qdrant_client  # noqa: F401
        import sentence_transformers  # noqa: F401
        import yaml  # noqa: F401

        return True, "Core dependencies installed"
    except ImportError as e:
        missing = str(e).split("'")[1] if "'" in str(e) else "unknown"
        return False, f"Missing dependency: {missing} (run setup-dev.sh)"


def check_qdrant_connection() -> tuple[bool, str]:
    """Check if Qdrant is accessible (optional)."""
    try:
        import requests

        response = requests.get("http://localhost:6333/health", timeout=2)
        if response.status_code == 200:
            return True, "Qdrant is running and accessible"
        return False, f"Qdrant returned status {response.status_code}"
    except ImportError:
        return False, "requests not installed (skip Qdrant check)"
    except Exception:
        return False, "Qdrant not accessible (optional - start with docker-compose)"


def main() -> int:
    """Run all environment validation checks."""
    print_status("🔍 Validating MCP Local LLM environment...\n")

    checks: list[tuple[str, tuple[bool, str], bool]] = [
        # (category, check_result, is_required)
        ("Python Version", check_python_version(), True),
        ("Virtual Environment", check_virtual_env(), True),
        (".env Configuration", check_env_file(), True),
        ("data/ Directory", check_directory_exists(Path("data"), "data/"), True),
        ("logs/ Directory", check_directory_exists(Path("logs"), "logs/"), True),
        ("policy/ Directory", check_directory_exists(Path("policy"), "policy/"), True),
        (
            "config.example.yaml",
            check_file_exists(Path("config.example.yaml"), "config.example.yaml"),
            True,
        ),
        ("Python Dependencies", check_dependencies(), True),
        ("Docker Availability", check_docker(), False),  # Optional
        ("Qdrant Connection", check_qdrant_connection(), False),  # Optional
    ]

    required_passed = 0
    required_total = 0
    optional_passed = 0
    optional_total = 0

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Required Checks:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    for category, (passed, message), is_required in checks:
        if is_required:
            required_total += 1
            if passed:
                required_passed += 1
                print_success(f"{category}: {message}")
            else:
                print_error(f"{category}: {message}")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Optional Checks:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    for category, (passed, message), is_required in checks:
        if not is_required:
            optional_total += 1
            if passed:
                optional_passed += 1
                print_success(f"{category}: {message}")
            else:
                print_warning(f"{category}: {message}")

    # Print summary
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Summary:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print(f"Required: {required_passed}/{required_total} passed")
    print(f"Optional: {optional_passed}/{optional_total} passed")

    if required_passed == required_total:
        print_success("\n✅ Environment validation PASSED!")
        print_status("You're ready to start development 🚀\n")
        return 0
    else:
        print_error(f"\n❌ Environment validation FAILED!")
        print_error(
            f"{required_total - required_passed} required checks failed\n"
        )
        print_status("Fix the issues above and run again: make validate-env\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

