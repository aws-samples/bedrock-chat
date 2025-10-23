import os
from itertools import islice

from app.utils import get_bedrock_agent_client

DOCUMENT_BUCKET = os.environ.get("DOCUMENT_BUCKET")
bedrock_agent = get_bedrock_agent_client()


def handler(event, context):
    match event["Action"]:
        case "Ingest":
            return handle_ingest(event)

        case "Check":
            return handle_check(event)

        case _ as e:
            raise Exception(f"Unknown action {e}")


def handle_ingest(event):
    knowledge_base_id = event["KnowledgeBaseId"]
    data_source_id = event["DataSourceId"]
    get_data_source_response = bedrock_agent.get_data_source(
        knowledgeBaseId=knowledge_base_id,
        dataSourceId=data_source_id,
    )
    data_source_type = get_data_source_response["dataSource"][
        "dataSourceConfiguration"
    ]["type"]

    data_source_files = event.get("Files")
    if data_source_type == "S3" and data_source_files:
        for data_source_file in data_source_files:
            user_id = data_source_file["OwnerUserId"]
            bot_id = data_source_file["BotId"]

            added_files = data_source_file["Added"]
            for i in range(0, len(added_files), 10):
                bedrock_agent.ingest_knowledge_base_documents(
                    knowledgeBaseId=knowledge_base_id,
                    dataSourceId=data_source_id,
                    documents=[
                        {
                            "content": {
                                "dataSourceType": "S3",
                                "s3": {
                                    "s3Location": {
                                        "uri": f"s3://{DOCUMENT_BUCKET}/{user_id}/{bot_id}/documents/{file}",
                                    },
                                },
                            },
                        }
                        for file in islice(added_files, i, i + 10)
                    ],
                )

            deleted_files = data_source_file["Deleted"]
            for i in range(0, len(deleted_files), 10):
                bedrock_agent.delete_knowledge_base_documents(
                    knowledgeBaseId=knowledge_base_id,
                    dataSourceId=data_source_id,
                    documentIdentifiers=[
                        {
                            "dataSourceType": "S3",
                            "s3": {
                                "uri": f"s3://{DOCUMENT_BUCKET}/{user_id}/{bot_id}/documents/{file}",
                            },
                        }
                        for file in islice(deleted_files, i, i + 10)
                    ],
                )

        return {
            "KnowledgeBaseId": knowledge_base_id,
            "DataSourceId": data_source_id,
            "Files": data_source_files,
            "IngestionJobId": None,
        }

    else:
        start_job_response = bedrock_agent.start_ingestion_job(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id,
        )
        ingestion_job_id = start_job_response["ingestionJob"]["ingestionJobId"]

        return {
            "KnowledgeBaseId": knowledge_base_id,
            "DataSourceId": data_source_id,
            "Files": None,
            "IngestionJobId": ingestion_job_id,
        }


class RetryException(Exception):
    pass


def handle_check(event):
    ingestion_job = event["IngestionJob"]
    knowledge_base_id = ingestion_job["KnowledgeBaseId"]
    data_source_id = ingestion_job["DataSourceId"]
    data_source_files = ingestion_job.get("Files")
    if data_source_files:
        for data_source_file in data_source_files:
            user_id = data_source_file["OwnerUserId"]
            bot_id = data_source_file["BotId"]

            added_files = data_source_file["Added"]
            for i in range(0, len(added_files), 10):
                get_documents_response = bedrock_agent.get_knowledge_base_documents(
                    knowledgeBaseId=knowledge_base_id,
                    dataSourceId=data_source_id,
                    documentIdentifiers=[
                        {
                            "dataSourceType": "S3",
                            "s3": {
                                "uri": f"s3://{DOCUMENT_BUCKET}/{user_id}/{bot_id}/documents/{file}",
                            },
                        }
                        for file in islice(added_files, i, i + 10)
                    ],
                )
                for document in get_documents_response["documentDetails"]:
                    status = document["status"]
                    uri = document["identifier"].get("s3", {})["uri"]
                    match status:
                        case "INDEXED":
                            pass

                        case (
                            "PENDING" | "STARTING" | "IN_PROGRESS" | "PARTIALLY_INDEXED"
                        ):
                            raise RetryException()

                        case _:
                            raise Exception(f"File {uri}: Bad status '{status}'.")

            deleted_files = data_source_file["Deleted"]
            for i in range(0, len(deleted_files), 10):
                get_documents_response = bedrock_agent.get_knowledge_base_documents(
                    knowledgeBaseId=knowledge_base_id,
                    dataSourceId=data_source_id,
                    documentIdentifiers=[
                        {
                            "dataSourceType": "S3",
                            "s3": {
                                "uri": f"s3://{DOCUMENT_BUCKET}/{user_id}/{bot_id}/documents/{file}",
                            },
                        }
                        for file in islice(deleted_files, i, i + 10)
                    ],
                )
                for document in get_documents_response["documentDetails"]:
                    status = document["status"]
                    uri = document["identifier"].get("s3", {})["uri"]
                    match status:
                        case "NOT_FOUND":
                            pass

                        case "PENDING" | "DELETING" | "DELETE_IN_PROGRESS":
                            raise RetryException()

                        case _:
                            raise Exception(f"File '{uri}': Bad status '{status}'.")

        return

    ingestion_job_id = ingestion_job.get("IngestionJobId")
    if ingestion_job_id:
        get_job_response = bedrock_agent.get_ingestion_job(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id,
            ingestionJobId=ingestion_job_id,
        )
        status = get_job_response["ingestionJob"]["status"]
        match status:
            case "COMPLETE":
                pass

            case "STARTING" | "IN_PROGRESS":
                raise RetryException()

            case _:
                raise Exception(
                    f"Ingestion Job '{ingestion_job_id}': Bad status '{status}'."
                )

        return

    raise Exception("Invalid parameters.")
