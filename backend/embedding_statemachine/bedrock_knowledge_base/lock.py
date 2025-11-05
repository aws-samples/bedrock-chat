import os

import boto3

BEDROCK_REGION = os.environ.get("BEDROCK_REGION")
DOCUMENT_BUCKET = os.environ["DOCUMENT_BUCKET"]

s3 = boto3.client(
    service_name="s3",
    region_name=BEDROCK_REGION,
)


def handler(event, context):
    """Distributed locking using Amazon S3's conditional write feature."""
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


def lock_name_to_s3_key(lock_name: str) -> str:
    return f".temp/.lock.{lock_name.lower()}"


def handle_acquire(event):
    """Acquire a distributed lock."""
    lock_file_key = lock_name_to_s3_key(event["LockName"])
    owner = event["Owner"]
    try:
        # Create the lock file only if it does not already exist. Content is the owner ID.
        response = s3.put_object(
            Bucket=DOCUMENT_BUCKET,
            Key=lock_file_key,
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
                    # Check the owner ID because there is a possibility that `PreconditionFailed` occurred due to a retry caused by a network error, etc.
                    get_response = s3.get_object(
                        Bucket=DOCUMENT_BUCKET,
                        Key=lock_file_key,
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
    """Release the acquired lock."""
    lock_file_key = lock_name_to_s3_key(event["LockName"])
    lock_id = event["LockId"]
    try:
        # Delete the lock file only if it have the same `ETag` as when it was created.
        # Note: lock is automatically released after 1 day passed (see also: cdk/lib/bedrock-region-resources.ts)
        s3.delete_object(
            Bucket=DOCUMENT_BUCKET,
            Key=lock_file_key,
            IfMatch=lock_id,
        )

    except s3.exceptions.ClientError as ex:
        error_code = ex.response.get("Error", {}).get("Code")
        match error_code:
            case "PreconditionFailed":
                # If the lock file was replaced by another owner, the release of the lock is considered successful.
                pass

            case "ConditionalRequestConflict":
                raise RetryException()

            case _:
                raise ex
