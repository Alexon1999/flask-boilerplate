#!/bin/bash

# Check if a file path is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: source ./loadenv.sh path_to_env_file"
    return 1  # Use 'return' instead of 'exit' to not terminate the current shell
fi

# Check if the file exists
if [ ! -f "$1" ]; then
    echo "Error: File not found!"
    return 1
fi

# Load the environment variables from the file
set -a  # Automatically export all variables
source "$1"
set +a  # Stop automatically exporting variables

echo "Environment variables loaded from $1"
