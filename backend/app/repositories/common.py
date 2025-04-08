import json
import os
from typing import Dict, List, Optional, Sequence
import logging

import boto3

# --- Troubleshooting Start: Log environment variables at import time ---
logger = logging.getLogger(__name__)
DDB_ENDPOINT_URL = os.environ.get("DDB_ENDPOINT_URL")
TABLE_NAME = os.environ.get("TABLE_NAME", "")
ACCOUNT = os.environ.get("ACCOUNT", "")
REGION = os.environ.get("REGION", "ap-northeast-1")
TABLE_ACCESS_ROLE_ARN = os.environ.get("TABLE_ACCESS_ROLE_ARN", "")
AWS_EXECUTION_ENV = os.environ.get("AWS_EXECUTION_ENV")

logger.debug(f"Common Repo Init - DDB_ENDPOINT_URL: '{DDB_ENDPOINT_URL}'")
logger.debug(f"Common Repo Init - TABLE_NAME: '{TABLE_NAME}'")
logger.debug(f"Common Repo Init - ACCOUNT: '{ACCOUNT}'")
logger.debug(f"Common Repo Init - REGION: '{REGION}'")
logger.debug(f"Common Repo Init - TABLE_ACCESS_ROLE_ARN: '{TABLE_ACCESS_ROLE_ARN}'")
logger.debug(f"Common Repo Init - AWS_EXECUTION_ENV: '{AWS_EXECUTION_ENV}'")
# --- Troubleshooting End ---

TRANSACTION_BATCH_SIZE = 25


class RecordNotFoundError(Exception):
    pass


class RecordAccessNotAllowedError(Exception):
    pass


class ResourceConflictError(Exception):
    pass


def compose_conv_id(user_id: str, conversation_id: str):
    # Add user_id prefix for row level security to match with `LeadingKeys` condition
    return f"{user_id}#CONV#{conversation_id}"


def decompose_conv_id(conv_id: str):
    return conv_id.split("#")[-1]


def compose_bot_id(user_id: str, bot_id: str):
    # Add user_id prefix for row level security to match with `LeadingKeys` condition
    return f"{user_id}#BOT#{bot_id}"


def decompose_bot_id(composed_bot_id: str):
    return composed_bot_id.split("#")[-1]


def compose_bot_alias_id(user_id: str, alias_id: str):
    # Add user_id prefix for row level security to match with `LeadingKeys` condition
    return f"{user_id}#BOT_ALIAS#{alias_id}"


def decompose_bot_alias_id(composed_alias_id: str):
    return composed_alias_id.split("#")[-1]


def compose_related_document_source_id(
    user_id: str,
    conversation_id: str,
    source_id: str,
):
    # Add user_id prefix for row level security to match with `LeadingKeys` condition
    return f"{user_id}#RELATED_DOCUMENT#{conversation_id}#{source_id}"


def decompose_related_document_source_id(composed_id: str):
    return composed_id.split("#")[-1]


def _get_aws_resource(service_name: str, user_id: Optional[str] = None):
    """Get AWS resource with optional row-level access control for DynamoDB.
    Ref: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_dynamodb_items.html
    """
    # --- Troubleshooting Start ---
    logger.debug(f"_get_aws_resource called for service: '{service_name}', user_id: '{user_id}'")
    # --- Troubleshooting End ---

    # Use the captured AWS_EXECUTION_ENV
    if not AWS_EXECUTION_ENV:
        if DDB_ENDPOINT_URL:
            # --- Troubleshooting Start ---
            logger.debug(f"Using local DDB endpoint: {DDB_ENDPOINT_URL}, region: {REGION}")
            # --- Troubleshooting End ---
            return boto3.resource(
                service_name,
                endpoint_url=DDB_ENDPOINT_URL,
                aws_access_key_id="key",
                aws_secret_access_key="key",
                region_name=REGION,
            )  # type: ignore[call-overload]
        else:
            # --- Troubleshooting Start ---
            logger.debug(f"Using default boto3 resource (no endpoint, not in AWS exec env), region: {REGION}")
            # --- Troubleshooting End ---
            return boto3.resource(service_name, region_name=REGION)  # type: ignore[call-overload]

    # --- Troubleshooting Start ---
    logger.debug(f"Running in AWS execution environment. Attempting role assumption.")
    if not TABLE_ACCESS_ROLE_ARN:
        logger.error("TABLE_ACCESS_ROLE_ARN is not set, but required in AWS execution environment. Cannot assume role.")
        raise ValueError("TABLE_ACCESS_ROLE_ARN environment variable is required.")
    if not TABLE_NAME:
        logger.error("TABLE_NAME is not set, but required for policy generation.")
        raise ValueError("TABLE_NAME environment variable is required.")
    if not ACCOUNT:
         logger.warning("ACCOUNT environment variable is not set. Policy generation might be incomplete if needed elsewhere.")
    # --- Troubleshooting End ---

    policy_document: Dict[str, List[Dict]] = {
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:BatchGetItem",
                    "dynamodb:BatchWriteItem",
                    "dynamodb:ConditionCheckItem",
                    "dynamodb:DeleteItem",
                    "dynamodb:DescribeTable",
                    "dynamodb:GetItem",
                    "dynamodb:GetRecords",
                    "dynamodb:PutItem",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:UpdateItem",
                ],
                "Resource": [
                    f"arn:aws:dynamodb:{REGION}:{ACCOUNT}:table/{TABLE_NAME}",
                    f"arn:aws:dynamodb:{REGION}:{ACCOUNT}:table/{TABLE_NAME}/index/*",
                ],
            }
        ]
    }

    # Commenting out the row-level security part as it was in the original code
    # if user_id:
    #     policy_document["Statement"][0]["Condition"] = {
    #         # Allow access to items with the same partition key as the user id
    #         "ForAllValues:StringLike": {"dynamodb:LeadingKeys": [f"{user_id}*"]}
    #     }

    # --- Troubleshooting Start ---
    logger.debug(f"Using Role ARN for AssumeRole: {TABLE_ACCESS_ROLE_ARN}")
    # Avoid logging the full policy if it could be sensitive, log resource part
    logger.debug(f"Policy Resources: {json.dumps(policy_document['Statement'][0]['Resource'])}")
    # --- Troubleshooting End ---
    try:
        sts_client = boto3.client("sts")
        assumed_role_object = sts_client.assume_role(
            RoleArn=TABLE_ACCESS_ROLE_ARN,
            RoleSessionName="DynamoDBSession",
            Policy=json.dumps(policy_document),
        )
        credentials = assumed_role_object["Credentials"]
        # --- Troubleshooting Start ---
        logger.debug(f"AssumeRole successful. Assumed Role User ARN: {assumed_role_object.get('AssumedRoleUser', {}).get('Arn')}")
        logger.debug(f"Credentials obtained - AccessKeyId: {credentials['AccessKeyId']}, Expiration: {credentials['Expiration']}")
        # --- Troubleshooting End ---
        session = boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
        # --- Troubleshooting Start ---
        logger.debug(f"Returning session resource for '{service_name}' with assumed credentials.")
        # --- Troubleshooting End ---
        return session.resource(service_name, region_name=REGION)  # type: ignore[call-overload]
    except Exception as e:
        logger.error(f"Failed to assume role {TABLE_ACCESS_ROLE_ARN}: {e}", exc_info=True)
        raise


def _get_dynamodb_client(user_id: Optional[str] = None):
    """Get a DynamoDB client, optionally with row-level access control."""
    # --- Troubleshooting Start ---
    logger.debug(f"_get_dynamodb_client called for user_id: '{user_id}'")
    # --- Troubleshooting End ---
    return _get_aws_resource("dynamodb", user_id=user_id).meta.client


def _get_table_client(user_id: str):
    """Get a DynamoDB table client with row-level access."""
    # --- Troubleshooting Start ---
    logger.debug(f"_get_table_client called for user_id: '{user_id}'. Will use TABLE_NAME: '{TABLE_NAME}'")
    if not TABLE_NAME:
         logger.error("_get_table_client: TABLE_NAME is empty. Cannot get table resource.")
         return None
    # --- Troubleshooting End ---
    try:
        dynamodb_resource = _get_aws_resource("dynamodb", user_id=user_id)
        return dynamodb_resource.Table(TABLE_NAME)
    except Exception as e:
         logger.error(f"Error getting table resource '{TABLE_NAME}' for user '{user_id}': {e}", exc_info=True)
         return None


def _get_table_public_client():
    """Get a DynamoDB table client.
    Warning: No row-level access. Use for only limited use case.
    """
    # --- Troubleshooting Start ---
    logger.debug(f"_get_table_public_client called. Will use TABLE_NAME: '{TABLE_NAME}'")
    if not TABLE_NAME:
         logger.error("_get_table_public_client: TABLE_NAME is empty. Cannot get public table resource.")
         return None
    # --- Troubleshooting End ---
    try:
        dynamodb_resource = _get_aws_resource("dynamodb")
        return dynamodb_resource.Table(TABLE_NAME)
    except Exception as e:
         logger.error(f"Error getting public table resource '{TABLE_NAME}': {e}", exc_info=True)
         return None
