#!/bin/bash

# Exit on any error
set -e

STACK_NAME=${1:-BedrockChatStack}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install it first."
    exit 1
fi

OUTPUT_BACKEND_FILE="backend/.env-backend.local"
OUTPUT_FRONTEND_FILE="frontend/.env-frontend.local"

# Get the AWS account number
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text 2>/dev/null) || {
    echo "Error: Failed to get AWS account ID. Please check your AWS credentials."
    exit 1
}

# Get CloudFormation outputs in JSON format
echo "Fetching CloudFormation stack outputs for: $STACK_NAME"
CF_OUTPUT=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --query "Stacks[0].Outputs" --output json 2>/dev/null) || {
    echo "Error: Failed to fetch CloudFormation outputs."
    echo "Please check:"
    echo "  - Your AWS CLI configuration"
    echo "  - Stack name: $STACK_NAME exists"
    echo "  - You have necessary permissions"
    exit 1
}

# Check if output files are writable before proceeding
if ! touch "$OUTPUT_BACKEND_FILE" 2>/dev/null; then
    echo "Error: Cannot write to $OUTPUT_BACKEND_FILE"
    exit 1
fi

if ! touch "$OUTPUT_FRONTEND_FILE" 2>/dev/null; then
    echo "Error: Cannot write to $OUTPUT_FRONTEND_FILE"
    exit 1
fi

# Parse the outputs and format them as .env key-value pairs
echo "# Environment variables from CloudFormation stack: $STACK_NAME" > "$OUTPUT_BACKEND_FILE"
echo "AWS_REGION=us-east-1" >> "$OUTPUT_BACKEND_FILE"
echo "ACCOUNT=$ACCOUNT_ID" >> "$OUTPUT_BACKEND_FILE"
echo "BEDROCK_REGION=us-east-1" >> "$OUTPUT_BACKEND_FILE"
echo "AWS_DEFAULT_REGION=us-east-1" >> "$OUTPUT_BACKEND_FILE"
echo "CLIENT_ID=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("AuthUserPoolClientId")).OutputValue' | head -n 1)" >> "$OUTPUT_BACKEND_FILE"
echo "DOCUMENT_BUCKET=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("DocumentBucketName")).OutputValue' | head -n 1)" >> "$OUTPUT_BACKEND_FILE"
echo "LARGE_MESSAGE_BUCKET=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("LargeMessageBucketName")).OutputValue' | head -n 1)" >> "$OUTPUT_BACKEND_FILE"
echo "REGION=us-east-1" >> "$OUTPUT_BACKEND_FILE"
echo "CORS_ALLOW_ORIGINS=*" >> "$OUTPUT_BACKEND_FILE"
echo "PORT=8000" >> "$OUTPUT_BACKEND_FILE"
echo "TABLE_NAME=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("ConversationTableName")).OutputValue' | head -n 1)" >> "$OUTPUT_BACKEND_FILE"
echo "TABLE_ACCESS_ROLE_ARN=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("TableAccessRoleArn")).OutputValue' | head -n 1)" >> "$OUTPUT_BACKEND_FILE"
echo "USAGE_ANALYSIS_WORKGROUP=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("UsageAnalysisUsageAnalysisWorkgroup")).OutputValue' | head -n 1)" >> "$OUTPUT_BACKEND_FILE"
echo "USAGE_ANALYSIS_TABLE=ddb_export" >> "$OUTPUT_BACKEND_FILE"
echo "USAGE_ANALYSIS_DATABASE=bedrockchatstack_usage_analysis" >> "$OUTPUT_BACKEND_FILE"
echo "USAGE_ANALYSIS_OUTPUT_LOCATION=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("UsageAnalysisUsageAnalysisOutputLocation")).OutputValue' | head -n 1)" >> "$OUTPUT_BACKEND_FILE"
echo "USER_POOL_ID=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("AuthUserPoolId")).OutputValue' | head -n 1)" >> "$OUTPUT_BACKEND_FILE"

# Please duplicate this file to ".env.local" for local development
# in production development, these values will be automatically set.
echo "# Environment variables from CloudFormation stack: $STACK_NAME" > "$OUTPUT_FRONTEND_FILE"
echo "VITE_APP_API_ENDPOINT=http://localhost:8000" >> "$OUTPUT_FRONTEND_FILE"
echo "VITE_APP_WS_ENDPOINT=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("WebSocketWebSocketEndpoint")).OutputValue' | head -n 1)" >> "$OUTPUT_FRONTEND_FILE"

echo "VITE_APP_USER_POOL_ID=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("AuthUserPoolId")).OutputValue' | head -n 1)" >> "$OUTPUT_FRONTEND_FILE"
echo "VITE_APP_USER_POOL_CLIENT_ID=$(echo "$CF_OUTPUT" | jq -r '.[] | select(.OutputKey | contains("AuthUserPoolClientId")).OutputValue' | head -n 1)" >> "$OUTPUT_FRONTEND_FILE"
echo "VITE_APP_REGION=us-east-1" >> "$OUTPUT_FRONTEND_FILE"
echo "VITE_APP_REDIRECT_SIGNIN_URL=http://localhost/" >> "$OUTPUT_FRONTEND_FILE"
echo "VITE_APP_REDIRECT_SIGNOUT_URL=http://localhost/" >> "$OUTPUT_FRONTEND_FILE"
echo "VITE_APP_COGNITO_DOMAIN=\"\"" >> "$OUTPUT_FRONTEND_FILE"
echo "VITE_APP_USE_STREAMING=false" >> "$OUTPUT_FRONTEND_FILE"
echo "VITE_APP_SOCIAL_PROVIDERS=\"\"" >> "$OUTPUT_FRONTEND_FILE"