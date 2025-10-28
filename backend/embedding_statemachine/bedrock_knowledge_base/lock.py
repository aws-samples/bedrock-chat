import os
from datetime import datetime, timedelta

import boto3

BEDROCK_REGION = os.environ.get("BEDROCK_REGION")
DOCUMENT_BUCKET = os.environ["DOCUMENT_BUCKET"]

s3 = boto3.client(
    service_name="s3",
    region_name=BEDROCK_REGION,
)


def handler(event, context):
    action = event["Action"]
    match action:
        case "Acquire":
            return handle_acquire(event)

        case "Release":
            return handle_release(event)

        case _:
            raise Exception(f"Invalid action {action}")


class RetryException(Exception):
    pass


def handle_acquire(event):
    lock_name = event["LockName"]
    owner = event["Owner"]
    expires_seconds = event["ExpiresSeconds"]
    try:
        response = s3.put_object(
            Bucket=DOCUMENT_BUCKET,
            Key=f".lock.{lock_name.lower()}",
            Expires=datetime.now() + timedelta(seconds=expires_seconds),
            IfNoneMatch="*",
            Body=owner,
        )
        etag = response["ETag"]

        return {
            "LockId": etag,
        }

    except s3.exceptions.ClientError as ex:
        error_code = ex.response.get("Error", {}).get("Code")
        match error_code:
            case "PreconditionFailed":
                try:
                    get_response = s3.get_object(
                        Bucket=DOCUMENT_BUCKET,
                        Key=f".lock.{lock_name.lower()}",
                    )
                    body = get_response["Body"].read().decode()
                    if body != owner:
                        raise RetryException()

                    etag = get_response["ETag"]
                    return {
                        "LockId": etag,
                    }

                except s3.exceptions.NoSuchKey:
                    raise RetryException()

            case "ConditionalRequestConflict":
                raise RetryException()

            case _:
                raise ex


def handle_release(event):
    lock_name = event["LockName"]
    lock_id = event["LockId"]
    try:
        s3.delete_object(
            Bucket=DOCUMENT_BUCKET,
            Key=f".lock.{lock_name.lower()}",
            IfMatch=lock_id,
        )

    except s3.exceptions.ClientError as ex:
        error_code = ex.response.get("Error", {}).get("Code")
        match error_code:
            case "PreconditionFailed":
                pass

            case "ConditionalRequestConflict":
                raise RetryException()

            case _:
                raise ex
