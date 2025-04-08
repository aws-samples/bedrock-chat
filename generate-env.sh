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

# Attempt to detect AWS region from AWS CLI configuration
AWS_REGION=$(aws configure get region 2>/dev/null) || AWS_REGION=""
if [ -z "$AWS_REGION" ]; then
    echo "Warning: Could not detect AWS region from AWS CLI configuration. Defaulting to us-east-1."
    AWS_REGION="us-east-1"
fi

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

# Function to get CloudFormation output value with fallback
# Usage: get_cf_output "OutputKeyName" ["FallbackSearchTerm"]
get_cf_output() {
    local key=$1
    local fallback=${2:-$1}
    
    # Try exact match first
    local value=$(echo "$CF_OUTPUT" | jq -r --arg key "$key" '.[] | select(.OutputKey == $key).OutputValue // empty')
    
    # If exact match fails and fallback term provided, try contains search
    if [ -z "$value" ]; then
        value=$(echo "$CF_OUTPUT" | jq -r --arg key "$fallback" '.[] | select(.OutputKey | contains($key)).OutputValue' | head -n 1)
    fi
    
    echo "$value"
}

# Parse CloudFormation outputs using our function
CLIENT_ID=$(get_cf_output "AuthUserPoolClientId")
DOCUMENT_BUCKET=$(get_cf_output "DocumentBucketName")
LARGE_MESSAGE_BUCKET=$(get_cf_output "LargeMessageBucketName")
TABLE_NAME=$(get_cf_output "ConversationTableName")
CONVERSATION_TABLE_NAME=$(get_cf_output "ConversationTableName")
TABLE_ACCESS_ROLE_ARN=$(get_cf_output "TableAccessRoleArn")
USAGE_ANALYSIS_WORKGROUP=$(get_cf_output "AnalyticsWorkgroup")
USAGE_ANALYSIS_OUTPUT_LOCATION=$(get_cf_output "AnalyticsOutputLocation")
BOTS_METADATA_TABLE_ARN=$(get_cf_output "BotsMetadataTableArn")
BOTS_METADATA_TABLE_NAME=$(echo "$BOTS_METADATA_TABLE_ARN" | awk -F'/' '{print $2}')
BOTS_METADATA_CONFIG_TABLE_ARN=$(get_cf_output "BotsMetadataConfigTableArn")
BOTS_METADATA_CONFIG_TABLE_NAME=$(get_cf_output "BotsMetadataConfigTableName")
BOTS_BUCKET_NAME=$(get_cf_output "BotsBucketName")
USER_POOL_ID=$(get_cf_output "AuthUserPoolId")
LTI_DATA_TABLE_NAME=$(get_cf_output "LtiDataTableName")
WEBSOCKET_ENDPOINT=$(get_cf_output "WebSocketWebSocketEndpoint")
DDB_BUCKET_NAME=$(get_cf_output "DdbBucketName")
USAGE_ANALYSIS_TABLE=$(get_cf_output "ConversationAnalyticsTable")
BOTS_ANALYTICS_TABLE_ARN=$(get_cf_output "BotsAnalyticsTableArn")

# Try to get Bing API secret ARN
BING_API_SECRET_ARN=$(aws secretsmanager describe-secret --secret-id 'bing-api-key' --query 'ARN' --output text 2>/dev/null) || {
    echo "Warning: 'bing-api-key' secret not found. Setting BING_API_SECRET_ARN to an empty value."
    BING_API_SECRET_ARN=""
}

# Calculate TABLE_ARN from account, region and table name
TABLE_ARN="arn:aws:dynamodb:${AWS_REGION}:${ACCOUNT_ID}:table/${TABLE_NAME}"

# Determine the usage analysis database name from stack name
USAGE_ANALYSIS_DATABASE="$(echo $STACK_NAME | tr '[:upper:]' '[:lower:]')_usage_analysis"

# Generate backend environment file with organized sections
cat > "$OUTPUT_BACKEND_FILE" << EOF
# Environment variables from CloudFormation stack: $STACK_NAME - Account: $ACCOUNT_ID

# ---------- AWS Configuration ----------
AWS_REGION=$AWS_REGION
ACCOUNT=$ACCOUNT_ID
BEDROCK_REGION=$AWS_REGION
AWS_DEFAULT_REGION=$AWS_REGION
REGION=$AWS_REGION

# ---------- API Server Configuration ----------
PORT=8000
HOST="0.0.0.0"
CORS_ALLOW_ORIGINS=*
CORS_ALLOW_CREDENTIALS=true
DEBUG=True
LOG_LEVEL=DEBUG
FRONTEND_URL=http://localhost:5173

# ---------- Authentication ----------
USER_POOL_ID=$USER_POOL_ID
CLIENT_ID=$CLIENT_ID

# ---------- Storage Configuration ----------
DOCUMENT_BUCKET=$DOCUMENT_BUCKET
LARGE_MESSAGE_BUCKET=$LARGE_MESSAGE_BUCKET
CONVERSATION_TABLE_NAME=$CONVERSATION_TABLE_NAME
TABLE_NAME=$TABLE_NAME
TABLE_ARN=$TABLE_ARN
TABLE_ACCESS_ROLE_ARN=$TABLE_ACCESS_ROLE_ARN
LTI_DATA_TABLE_NAME=$LTI_DATA_TABLE_NAME
BOTS_METADATA_TABLE_ARN=$BOTS_METADATA_TABLE_ARN
BOTS_METADATA_TABLE_NAME=$BOTS_METADATA_TABLE_NAME
BOTS_METADATA_CONFIG_TABLE_ARN=$BOTS_METADATA_CONFIG_TABLE_ARN
BOTS_METADATA_CONFIG_TABLE_NAME=$BOTS_METADATA_CONFIG_TABLE_NAME

# ---------- Analytics Configuration ----------
USAGE_ANALYSIS_WORKGROUP=$USAGE_ANALYSIS_WORKGROUP
USAGE_ANALYSIS_TABLE=$USAGE_ANALYSIS_TABLE
USAGE_ANALYSIS_DATABASE=$USAGE_ANALYSIS_DATABASE
USAGE_ANALYSIS_OUTPUT_LOCATION=$USAGE_ANALYSIS_OUTPUT_LOCATION
USAGE_ANALYSIS_BUCKET=$DDB_BUCKET_NAME
BOTS_BUCKET_NAME=$BOTS_BUCKET_NAME
BOTS_ANALYTICS_TABLE_ARN=$BOTS_ANALYTICS_TABLE_ARN

# ---------- External Services ----------
BING_API_SECRET_ARN=$BING_API_SECRET_ARN
EOF

# Generate frontend environment file
cat > "$OUTPUT_FRONTEND_FILE" << EOF
# Environment variables from CloudFormation stack: $STACK_NAME - Account: $ACCOUNT_ID

# ---------- API Configuration ----------
VITE_APP_API_ENDPOINT=http://localhost:8000
VITE_APP_WS_ENDPOINT=$WEBSOCKET_ENDPOINT

# ---------- Authentication ----------
VITE_APP_USER_POOL_ID=$USER_POOL_ID
VITE_APP_USER_POOL_CLIENT_ID=$CLIENT_ID
VITE_APP_REGION=$AWS_REGION
VITE_APP_REDIRECT_SIGNIN_URL=http://localhost/
VITE_APP_REDIRECT_SIGNOUT_URL=http://localhost/
VITE_APP_COGNITO_DOMAIN=""
VITE_APP_SOCIAL_PROVIDERS=""

# ---------- App Features ----------
VITE_APP_USE_STREAMING=false
EOF

echo "Environment files generated successfully!"
echo "Backend: $OUTPUT_BACKEND_FILE"
echo "Frontend: $OUTPUT_FRONTEND_FILE"
