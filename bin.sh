#!/bin/bash
echo "############################################################################"
echo "###                                                                      ###"
echo "###           ⚠️  Caution: A Whole New World with v2.x Awaits!  ⚠️          ###"
echo "###                                                                      ###"
echo "###  🚨 v2.x is NOT compatible with any older versions like v1.x or below. 🚨  ###"
echo "###  You must read the migration guide carefully before proceeding:       ###"
echo "###  https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/migration/V1_TO_V2.md  ###"
echo "###                                                                      ###"
echo "###  This isn't just a regular upgrade. Data preservation requires        ###"
echo "###  following specific steps, or you may risk CUSTOMIZED BOT LOSS.      ###"
echo "###                                                                      ###"
echo "###  💡 This script is only for new users or those already on v2.x.        ###"
echo "###  If that's you, let's get started! Otherwise, check the guide first.  ###"
echo "###                                                                      ###"
echo "############################################################################"
echo ""
while true; do
    read -p "Are you ready to explore the world of v2.x? (y/N): " answer
    case ${answer:0:1} in
        y|Y )
            echo "Buckle up! Starting deployment for v2.x..."
            break
            ;;
        n|N )
            echo "Whoa, hold on! This script is only for v2.x users. Please refer to the migration guide if you're coming from an older version."
            exit 1
            ;;
        * )
            echo "Let's keep it simple. Please enter y or n."
            ;;
    esac
done


# Default parameters
ALLOW_SELF_REGISTER="true"
ENABLE_LAMBDA_SNAPSTART="false"
IPV4_RANGES=""
IPV6_RANGES=""
DISABLE_IPV6="false"
ALLOWED_SIGN_UP_EMAIL_DOMAINS=""
BEDROCK_REGION="us-east-1"
CDK_JSON_OVERRIDE="{}"
REPO_URL="https://github.com/aws-samples/bedrock-claude-chat.git"
VERSION="v2"

# Parse command-line arguments for customization
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --disable-self-register) ALLOW_SELF_REGISTER="false" ;;
        --enable-lambda-snapstart) ENABLE_LAMBDA_SNAPSTART="true" ;;
        --disable-ipv6) DISABLE_IPV6="true" ;;
        --ipv4-ranges) IPV4_RANGES="$2"; shift ;;
        --ipv6-ranges) IPV6_RANGES="$2"; shift ;;
        --bedrock-region) BEDROCK_REGION="$2"; shift ;;
        --allowed-signup-email-domains) ALLOWED_SIGN_UP_EMAIL_DOMAINS="$2"; shift ;;
        --cdk-json-override) CDK_JSON_OVERRIDE="$2"; shift ;;
        --repo-url) REPO_URL="$2"; shift ;;
        --version) VERSION="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done


# Validate the template
aws cloudformation validate-template --template-body file://deploy.yml  > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "Template validation failed"
    exit 1
fi

StackName="CodeBuildForDeploy"

# Deploy the CloudFormation stack
aws cloudformation deploy \
  --stack-name $StackName \
  --template-file deploy.yml \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    AllowSelfRegister=$ALLOW_SELF_REGISTER \
    EnableLambdaSnapStart=$ENABLE_LAMBDA_SNAPSTART \
    DisableIpv6=$DISABLE_IPV6 \
    Ipv4Ranges="$IPV4_RANGES" \
    Ipv6Ranges="$IPV6_RANGES" \
    AllowedSignUpEmailDomains="$ALLOWED_SIGN_UP_EMAIL_DOMAINS" \
    BedrockRegion="$BEDROCK_REGION" \
    CdkJsonOverride="$CDK_JSON_OVERRIDE" \
    RepoUrl="$REPO_URL" \
    Version="$VERSION"

echo "Waiting for the stack creation to complete..."
echo "NOTE: this stack contains CodeBuild project which will be used for cdk deploy."
spin='-\|/'
i=0
while true; do
    status=$(aws cloudformation describe-stacks --stack-name $StackName --query 'Stacks[0].StackStatus' --output text 2>/dev/null)
    if [[ "$status" == "CREATE_COMPLETE" || "$status" == "UPDATE_COMPLETE" || "$status" == "DELETE_COMPLETE" ]]; then
        break
    elif [[ "$status" == "ROLLBACK_COMPLETE" || "$status" == "DELETE_FAILED" || "$status" == "CREATE_FAILED" ]]; then
        echo "Stack creation failed with status: $status"
        exit 1
    fi
    printf "\r${spin:i++%${#spin}:1}"
    sleep 1
done
echo -e "\nDone.\n"

outputs=$(aws cloudformation describe-stacks --stack-name $StackName --query 'Stacks[0].Outputs')
projectName=$(echo $outputs | jq -r '.[] | select(.OutputKey=="ProjectName").OutputValue')

if [[ -z "$projectName" ]]; then
    echo "Failed to retrieve the CodeBuild project name"
    exit 1
fi

echo "Starting CodeBuild project: $projectName..."
buildId=$(aws codebuild start-build --project-name $projectName --query 'build.id' --output text)

if [[ -z "$buildId" ]]; then
    echo "Failed to start CodeBuild project"
    exit 1
fi

echo "Waiting for the CodeBuild project to complete..."
while true; do
    buildStatus=$(aws codebuild batch-get-builds --ids $buildId --query 'builds[0].buildStatus' --output text)
    if [[ "$buildStatus" == "SUCCEEDED" || "$buildStatus" == "FAILED" || "$buildStatus" == "STOPPED" ]]; then
        break
    fi
    sleep 10
done
echo "CodeBuild project completed with status: $buildStatus"

buildDetail=$(aws codebuild batch-get-builds --ids $buildId --query 'builds[0].logs.{groupName: groupName, streamName: streamName}' --output json)

logGroupName=$(echo $buildDetail | jq -r '.groupName')
logStreamName=$(echo $buildDetail | jq -r '.streamName')

echo "Build Log Group Name: $logGroupName"
echo "Build Log Stream Name: $logStreamName"

echo "Fetch CDK deployment logs..."
logs=$(aws logs get-log-events --log-group-name $logGroupName --log-stream-name $logStreamName)
frontendUrl=$(echo "$logs" | grep -o 'FrontendURL = [^ ]*' | cut -d' ' -f3 | tr -d '\n,')

echo "Frontend URL: $frontendUrl"
