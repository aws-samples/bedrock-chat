#!/bin/bash

# Path to the .env-backend.local file
ENV_FILE="./.env-backend.local"

# Check if the .env-backend.local file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "Environment file $ENV_FILE not found!"
  exit 1
fi

# Export environment variables from the .env-backend.local file
export $(grep -v '^#' "$ENV_FILE" | xargs)

# Run the program
exec python  -m uvicorn app.main:app --port $PORT  
