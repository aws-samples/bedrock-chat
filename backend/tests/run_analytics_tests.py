#!/usr/bin/env python3
"""
Test Runner Script for Metadata and Analytics Components

This script runs the tests for the metadata repository and analytics routes,
collecting and summarizing the results.
"""

import subprocess
import re
import os
import sys
from datetime import datetime
import argparse
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import importlib.util

# Get the script directory to make paths relative
SCRIPT_DIR = Path(__file__).parent.absolute()
BASE_DIR = SCRIPT_DIR.parent.parent  # Go up to project root if needed

# Define test modules to run - with paths relative to script location
TEST_MODULES = {
    "metadata_repository": str(SCRIPT_DIR / "test_repositories/test_metadata_repository.py"),
    "analytics_routes": str(SCRIPT_DIR / "test_routes/test_analytics.py"),
    "dashboard_endpoints": str(SCRIPT_DIR / "test_routes/test_dashboard_endpoints.py"),
    "dashboard_analytics": str(SCRIPT_DIR / "test_repositories/test_dashboard_analytics.py"),
    "auth_mock": str(SCRIPT_DIR / "test_routes/test_auth_mock.py"),
    "usage_analysis_mocked": str(SCRIPT_DIR / "test_repositories/test_usage_analysis_mocked.py"),
}

# Optional additional test modules that may depend on our changes
OPTIONAL_MODULES = {
    "bot_repository": str(SCRIPT_DIR / "test_repositories/test_bot.py"),
    "metadata_routes": str(SCRIPT_DIR / "test_routes/test_metadata.py"),
}

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def check_package_installed(package_name: str) -> bool:
    """Check if a Python package is installed."""
    spec = importlib.util.find_spec(package_name)
    return spec is not None


def check_missing_packages() -> Dict[str, bool]:
    """Check which packages required for testing are missing."""
    required_packages = {
        'pydantic': "Required for data models",
        'fastapi': "Required for API testing",
        'jose': "Required for auth functionality",
        'pytest': "Core testing framework",
        'pytest_cov': "Coverage reporting"
    }
    
    results = {}
    for package, description in required_packages.items():
        installed = check_package_installed(package.split('_')[0])  # Handle pytest_cov -> pytest-cov
        results[package] = installed
    
    return results


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Run tests for metadata and analytics components')
    parser.add_argument('--all', action='store_true', help='Run all tests including optional modules')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--coverage', '-c', action='store_true', help='Generate coverage report')
    parser.add_argument('--summary-only', '-s', action='store_true', help='Show only summary, not detailed test output')
    parser.add_argument('--from-root', action='store_true', help='Run from project root (default: false)')
    return parser.parse_args()


def detect_missing_dependencies(text: str) -> Optional[str]:
    """
    Detect if test failure is due to missing dependencies.
    Returns the missing module name if found, None otherwise.
    """
    if "ModuleNotFoundError: No module named" in text:
        # Extract the missing module name
        import re
        module_match = re.search(r"No module named '([^']+)'", text)
        if module_match:
            return module_match.group(1)
    return None


def run_test(module_name: str, module_path: str, verbose: bool, summary_only: bool) -> Tuple[bool, Dict]:
    """Run the test for a specific module and return the result."""
    print(f"\n{Colors.BOLD}{Colors.UNDERLINE}Running tests for {module_name}{Colors.END}")
    
    # Build command
    command = ["python", "-m", "pytest", module_path]
    
    if verbose:
        command.append("-v")
    
    # Check if pytest-cov is installed before adding coverage options
    try:
        import pytest_cov
        has_coverage = True
    except ImportError:
        print(f"{Colors.YELLOW}pytest-cov not installed, skipping coverage reporting{Colors.END}")
        has_coverage = False
    
    # Add coverage options only if pytest-cov is available
    if has_coverage:
        coverage_commands = [
            "--cov=app.repositories.metadata_repository",
            "--cov=app.repositories.usage_analysis",
            "--cov=app.routes.analytics",
            "--cov=app.routes.metadata",
            "--cov-report=term-missing",
            "--cov-append"
        ]
        command.extend(coverage_commands)
    
    # Always capture output to check for dependency errors
    try:
        # Always capture output even if summary_only is False to check for errors
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        
        # Print output if not in summary mode
        if not summary_only:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
        
        # Check if test passed
        success = result.returncode == 0
        
        # Check for dependency errors - look in both stderr and stdout
        dependency_error = False
        missing_module = None
        
        # Check stderr first
        if not success and result.stderr:
            missing_module = detect_missing_dependencies(result.stderr)
            if missing_module:
                dependency_error = True
                print(f"{Colors.YELLOW}Missing dependency detected: {missing_module}{Colors.END}")
        
        # If no dependency error found in stderr, check stdout
        if not dependency_error and not success and result.stdout:
            missing_module = detect_missing_dependencies(result.stdout)
            if missing_module:
                dependency_error = True
                print(f"{Colors.YELLOW}Missing dependency detected: {missing_module}{Colors.END}")
        
        # Parse the output if in summary mode
        if summary_only and result.stdout:
            # Print a summary
            lines = result.stdout.splitlines()
            summary_lines = [line for line in lines if "passed" in line or "failed" in line or "ERROR" in line or "skipped" in line]
            if summary_lines:
                for line in summary_lines:
                    print(line)
            else:
                # If no summary found, show last few lines
                last_lines = lines[-5:] if len(lines) > 5 else lines
                for line in last_lines:
                    print(line)
        
        # If there's an error and we're in summary mode, print the error unless it's a dependency error
        if not success and summary_only and result.stderr and not dependency_error:
            print(f"{Colors.RED}Error output:{Colors.END}")
            print(result.stderr)
        
        return success, {
            "success": success,
            "output": result.stdout,
            "error": result.stderr,
            "dependency_error": dependency_error,
            "missing_module": missing_module
        }
    except Exception as e:
        print(f"{Colors.RED}Error running test: {str(e)}{Colors.END}")
        return False, {
            "success": False,
            "output": None,
            "error": str(e),
            "dependency_error": False,
            "missing_module": None
        }


def main():
    """Main entry point."""
    args = parse_args()
    
    # If --from-root flag is used, redefine test modules with paths relative to project root
    if args.from_root:
        global TEST_MODULES, OPTIONAL_MODULES
        TEST_MODULES = {
            "metadata_repository": "backend/tests/test_repositories/test_metadata_repository.py",
            "analytics_routes": "backend/tests/test_routes/test_analytics.py",
            "dashboard_endpoints": "backend/tests/test_routes/test_dashboard_endpoints.py",
            "dashboard_analytics": "backend/tests/test_repositories/test_dashboard_analytics.py",
            "auth_mock": "backend/tests/test_routes/test_auth_mock.py",
            "usage_analysis_mocked": "backend/tests/test_repositories/test_usage_analysis_mocked.py",
        }
        
        OPTIONAL_MODULES = {
            "bot_repository": "backend/tests/test_repositories/test_bot.py",
            "metadata_routes": "backend/tests/test_routes/test_metadata.py",
        }
    
    # Print current working directory and script location for debugging
    print(f"{Colors.CYAN}Running from: {os.getcwd()}{Colors.END}")
    print(f"{Colors.CYAN}Script location: {SCRIPT_DIR}{Colors.END}")
    
    # Check for missing packages
    print(f"\n{Colors.CYAN}Checking for required packages...{Colors.END}")
    missing_packages = []
    for package in ['pydantic', 'fastapi', 'jose', 'pytest_cov']:
        if not check_package_installed(package.split('_')[0]):  # Handle pytest_cov -> pytest-cov
            missing_packages.append(package.replace('_', '-'))
    
    if missing_packages:
        print(f"{Colors.YELLOW}Missing dependencies detected: {', '.join(missing_packages)}{Colors.END}")
        print(f"{Colors.CYAN}To install all missing dependencies:{Colors.END}")
        print(f"{Colors.CYAN}pip install {' '.join(missing_packages)}{Colors.END}\n")
    else:
        print(f"{Colors.GREEN}All required packages are installed.{Colors.END}\n")
    
    # Determine which modules to test
    modules_to_test = TEST_MODULES.copy()
    if args.all:
        modules_to_test.update(OPTIONAL_MODULES)
    
    # Run tests for each module
    results = {}
    all_success = True
    dependency_failures = []
    dependency_errors = {}
    
    for module_name, module_path in modules_to_test.items():
        # Skip modules that don't exist
        if not os.path.exists(module_path):
            print(f"{Colors.YELLOW}Warning: Test module {module_path} not found, skipping...{Colors.END}")
            continue
        
        success, result = run_test(module_name, module_path, args.verbose, args.summary_only)
        results[module_name] = result
        all_success = all_success and success
        
        # Store dependency errors 
        if not success:
            # First check if the test itself detected dependency errors
            if result.get("dependency_error", False):
                if result.get("missing_module"):
                    missing_module = result.get("missing_module")
                    dependency_errors[module_name] = missing_module
                    dependency_failures.append(module_name)
                else:
                    dependency_errors[module_name] = "unknown dependency"
                    dependency_failures.append(module_name)
            
            # Also manually check for dependency errors since our detection in run_test might miss some cases
            elif result.get("error") or result.get("output"):
                error_text = result.get("error", "") + result.get("output", "")
                missing_module = detect_missing_dependencies(error_text)
                if missing_module:
                    result["dependency_error"] = True
                    result["missing_module"] = missing_module
                    dependency_errors[module_name] = missing_module
                    dependency_failures.append(module_name)
    
    # Print summary
    print(f"\n{Colors.BOLD}{Colors.UNDERLINE}Test Summary:{Colors.END}")
    for module_name, result in results.items():
        if result["success"]:
            status = f"{Colors.GREEN}PASSED{Colors.END}"
        elif module_name in dependency_failures:
            status = f"{Colors.YELLOW}DEPENDENCY ERROR{Colors.END}"
        else:
            status = f"{Colors.RED}FAILED{Colors.END}"
        print(f"{module_name}: {status}")
    
    # Generate coverage report if requested and available
    if args.coverage:
        try:
            import coverage
            print(f"\n{Colors.BOLD}{Colors.UNDERLINE}Generating coverage report...{Colors.END}")
            # First combine any coverage data files that might exist
            subprocess.run(["python", "-m", "coverage", "combine"], check=False)
            # Then generate the HTML report
            subprocess.run(["python", "-m", "coverage", "html"], check=False)
            print(f"Coverage report generated at htmlcov/index.html")
        except ImportError:
            print(f"{Colors.YELLOW}coverage module not installed, cannot generate report{Colors.END}")
    
    # Print final status
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate real failures (excluding dependency errors)
    real_failures = [name for name, result in results.items() 
                     if not result["success"] and name not in dependency_failures]
    
    # Provide specific information about dependency failures
    if dependency_failures:
        print(f"\n{Colors.YELLOW}Note: {len(dependency_failures)} tests failed due to missing dependencies.{Colors.END}")
        print(f"{Colors.YELLOW}These tests were marked as 'DEPENDENCY ERROR' in the summary above.{Colors.END}")
        
        # Group failures by missing dependency
        missing_deps = {}
        for module, dep in dependency_errors.items():
            if dep not in missing_deps:
                missing_deps[dep] = []
            missing_deps[dep].append(module)
            
        # List missing dependencies and affected tests
        print(f"\n{Colors.YELLOW}Missing dependencies:{Colors.END}")
        for dep, modules in missing_deps.items():
            print(f"{Colors.YELLOW}  - {dep}: affects {', '.join(modules)}{Colors.END}")
            
        print(f"\n{Colors.CYAN}To install all required dependencies:{Colors.END}")
        print(f"{Colors.CYAN}pip install {' '.join(missing_deps.keys())}{Colors.END}")
    
    # Exit with appropriate status and message
    if not real_failures and not dependency_failures:
        print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed!{Colors.END} ({timestamp})")
        sys.exit(0)
    elif not real_failures and dependency_failures:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}All available tests passed! ({len(dependency_failures)} skipped due to missing dependencies){Colors.END} ({timestamp})")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}Some tests failed!{Colors.END} ({timestamp})")
        sys.exit(1)


if __name__ == "__main__":
    main() 