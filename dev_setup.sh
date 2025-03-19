#!/bin/bash

# Exit script on any error
set -e

LOG_FILE="dev_setup.log"

log() {
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$TIMESTAMP [$1] $2" | tee -a "$LOG_FILE"
}

handle_error() {
    log "ERROR" "$1"
    log "ERROR" "--- Exiting ---"
    exit 1
}

trap 'handle_error "Unexpected error occurred. Exiting..."' ERR

log "INFO" "--- Setting up Development Environment ---"

# Ensure Python 3 is installed
if ! command -v python3 &> /dev/null; then
    handle_error "Python 3 is not installed or not in PATH."
fi

# Create or recreate the virtual environment
log "INFO" "1. Setting up virtual environment..."
if [ -d ".venv" ]; then
    log "WARNING" "Existing virtual environment found. Removing..."
    rm -rf .venv || handle_error "Failed to remove existing virtual environment."
fi

python3 -m venv .venv || handle_error "Failed to create virtual environment."
source .venv/bin/activate

# Upgrade pip and install dependencies
log "INFO" "2. Installing dependencies..."
pip install --upgrade pip wheel || handle_error "Failed to upgrade pip."
pip install -r requirements-dev.txt || handle_error "Failed to install dependencies."

log "INFO" "--- ✅ Development setup complete! ---"

# Load environment variables if .env.development exists
if [ -f .env.development ]; then
    log "INFO" "Loading environment variables from .env.development"
        while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ ! "$line" =~ ^# && "$line" =~ = ]]; then
            var_name=$(echo "$line" | cut -d= -f1)
            var_value=$(echo "$line" | cut -d= -f2-)
            export "$var_name=$var_value" || log "ERROR" "Error in setting env variables." 
        fi
        done < .env.development
else
    log "WARNING" "No .env.development file found. Using system environment variables."
fi

# Ensure Flask is installed
if ! pip show flask &> /dev/null; then
    handle_error "Flask is not installed. Run 'pip install flask'."
fi

# Start the Flask app
log "INFO" "🌍 Starting Flask server..."
export FLASK_APP=run.py

# start the Flask development server
exec flask run --reload