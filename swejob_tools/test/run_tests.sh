#!/bin/bash


# Set PYTHONPATH to include the parent directory
export PYTHONPATH="$PYTHONPATH:$(dirname "$(dirname "$(pwd)")")"

# Run the specified Python script, or default to misc_tools_Test.py
SCRIPT=${1:-misc_tools_test.py}
python3 "$SCRIPT"

