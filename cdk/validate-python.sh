#!/bin/bash
set -eu  
PYTHON_FILES_DIR=".."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "🔍 Starting Lambda code validation..."

# Setup virtual environment if needed
setup_env() {
    if [ ! -d "$SCRIPT_DIR/.venv" ]; then
        python -m venv "$SCRIPT_DIR/.venv"
        source "$SCRIPT_DIR/.venv/bin/activate"
        pip install pylint
    else 
        source "$SCRIPT_DIR/.venv/bin/activate"
    fi
}

# Find Lambda handler files
find_lambda_files() {
    # Only check backend Lambda handlers and their supporting modules
    find "$PYTHON_FILES_DIR" -name "*.py" -type f \
        -not -path "*/\.*" \
        -not -path "*/tests/*" \
        -not -path "*/cdk.out/*" \
        -not -path "*/node_modules/*" \
        -not -path "*/cdk/lib/*" \
        -not -path "*/cdk/bin/*" \
        -not -path "*/.venv/*"
}

# Create minimal .pylintrc
create_pylint_config() {
    cat > "$SCRIPT_DIR/.pylintrc" << EOL
[MASTER]
ignore=CVS,tests,*.pyc,__pycache__,cdk.out,.venv
ignored-modules=boto3,pydantic,jose,fastapi,starlette,ulid,duckduckgo_search,retry,humps,aws_lambda_powertools,mypy_boto3_bedrock_runtime,mypy_boto3_bedrock_agent_runtime

[MESSAGES CONTROL]
disable=all
enable=E0602,  # Undefined variable
       E0603,  # Undefined all variable 
       E1120,  # No value for param 
       E0611,  # No name in module
       E1102,  # Not callable
       E1111,  # Assignment to function
       F0001,  # Syntax error
       E0633,  # Attempting to unpack non-sequence
       E0632   # Possible unbalanced tuple unpacking

[VARIABLES]
allow-global-unused-variables=no

[FORMAT]
max-line-length=120
EOL
}

# Create custom checker for iterator misuse
create_custom_checker() {
    cat > "$SCRIPT_DIR/iterator_checker.py" << EOL
from pylint.checkers import BaseChecker
from astroid import nodes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pylint.lint import PyLinter

class IteratorMisuseChecker(BaseChecker):
    name = 'iterator-misuse'
    priority = -1
    msgs = {
        'E9901': (
            'Iterator variable used as iterable in comprehension',
            'iterator-variable-misuse',
            'Iterator variable should not be used as the iterable in the same comprehension'
        ),
    }

    def visit_listcomp(self, node: nodes.ListComp) -> None:
        for generator in node.generators:
            target_names = {name.name for name in generator.target.nodes_of_class(nodes.Name)}
            iter_names = {name.name for name in generator.iter.nodes_of_class(nodes.Name)}
            if target_names & iter_names:
                self.add_message('E9901', node=node)

def register(linter: "PyLinter") -> None:
    """Register the checker."""
    linter.register_checker(IteratorMisuseChecker(linter))
EOL

    # Update pylintrc to load custom checker
    echo "load-plugins=iterator_checker" >> "$SCRIPT_DIR/.pylintrc"
}

# Run basic syntax check
run_syntax_check() {
    echo "Running syntax check..."
    python_files=$(find_lambda_files)
    if [ -z "$python_files" ]; then
        echo "⚠️ No Python files found to validate"
        return 0
    fi
    
    # Suppress warnings, only show errors
    python -W ignore -m py_compile $python_files || {
        echo "❌ Syntax error found"
        exit 1
    }
    echo "✅ Basic syntax check passed"
}

# Run minimal pylint
run_minimal_pylint() {
    echo "Running critical error checks..."
    python_files=$(find_lambda_files)
    create_pylint_config
    create_custom_checker
    
    PYTHONPATH="$SCRIPT_DIR" pylint --rcfile="$SCRIPT_DIR/.pylintrc" $python_files || {
        # Only fail on errors (exit code 1-31)
        if [ $? -le 31 ]; then
            echo "❌ Critical errors found (undefined variables/imports/iterator misuse)"
            exit 1
        fi
    }
    echo "✅ No critical errors found"
}

main() {
    setup_env
    run_syntax_check
    run_minimal_pylint
}

main || {
    echo "❌ Validation failed"
    exit 1
}
