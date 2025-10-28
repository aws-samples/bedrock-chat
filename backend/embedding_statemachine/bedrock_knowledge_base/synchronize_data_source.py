import os
from itertools import islice
from typing import TypedDict

from app.utils import (
    compose_upload_document_s3_path,
    get_bedrock_agent_client,
)

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


class DocumentsDiff(TypedDict):
    Added: list[str]
    Deleted: list[str]


def compose_upload_document_s3_uri(user_id: str, bot_id: str, filename: str) -> str:
    return f"s3://{DOCUMENT_BUCKET}/{compose_upload_document_s3_path(user_id, bot_id, filename)}"


def get_data_source_type(knowledge_base_id: str, data_source_id: str):
    get_data_source_response = bedrock_agent.get_data_source(
        knowledgeBaseId=knowledge_base_id,
        dataSourceId=data_source_id,
    )
    return get_data_source_response["dataSource"]["dataSourceConfiguration"]["type"]


def handle_ingest(event):
    knowledge_base_id = event["KnowledgeBaseId"]
    data_source_id = event["DataSourceId"]

    bot_files_diffs = event.get("FilesDiffs")
    if (
        bot_files_diffs
        and get_data_source_type(
            knowledge_base_id=knowledge_base_id,
            data_source_id=data_source_id,
        )
        == "S3"
    ):
        added_documents: list[str] = []
        unchanged_documents: list[str] = []
        deleted_documents: list[str] = []

        for bot_files_diff in bot_files_diffs:
            user_id = bot_files_diff["OwnerUserId"]
            bot_id = bot_files_diff["BotId"]

            added_documents.extend(
                compose_upload_document_s3_uri(user_id, bot_id, added_file)
                for added_file in bot_files_diff["Added"]
            )
            unchanged_documents.extend(
                compose_upload_document_s3_uri(user_id, bot_id, unchanged_file)
                for unchanged_file in bot_files_diff["Unchanged"]
            )
            deleted_documents.extend(
                compose_upload_document_s3_uri(user_id, bot_id, deleted_file)
                for deleted_file in bot_files_diff["Deleted"]
            )

        for i in range(0, len(unchanged_documents), 10):
            get_documents_response = bedrock_agent.get_knowledge_base_documents(
                knowledgeBaseId=knowledge_base_id,
                dataSourceId=data_source_id,
                documentIdentifiers=[
                    {
                        "dataSourceType": "S3",
                        "s3": {
                            "uri": document_identifier,
                        },
                    }
                    for document_identifier in islice(unchanged_documents, i, i + 10)
                ],
            )
            added_documents.extend(
                document["identifier"]["s3"]["uri"]
                for document in get_documents_response["documentDetails"]
                if document["status"] == "NOT_FOUND" and "s3" in document["identifier"]
            )

        documents_diff: DocumentsDiff = {
            "Added": [],
            "Deleted": [],
        }

        for i in range(0, len(added_documents), 10):
            ingest_response = bedrock_agent.ingest_knowledge_base_documents(
                knowledgeBaseId=knowledge_base_id,
                dataSourceId=data_source_id,
                documents=[
                    {
                        "content": {
                            "dataSourceType": "S3",
                            "s3": {
                                "s3Location": {
                                    "uri": document_identifier,
                                },
                            },
                        },
                    }
                    for document_identifier in islice(added_documents, i, i + 10)
                ],
            )
            documents_diff["Added"].extend(
                document["identifier"]["s3"]["uri"]
                for document in ingest_response["documentDetails"]
                if document["status"] != "IGNORED" and "s3" in document["identifier"]
            )

        for i in range(0, len(deleted_documents), 10):
            delete_response = bedrock_agent.delete_knowledge_base_documents(
                knowledgeBaseId=knowledge_base_id,
                dataSourceId=data_source_id,
                documentIdentifiers=[
                    {
                        "dataSourceType": "S3",
                        "s3": {
                            "uri": document_identifier,
                        },
                    }
                    for document_identifier in islice(deleted_documents, i, i + 10)
                ],
            )
            documents_diff["Deleted"].extend(
                document["identifier"]["s3"]["uri"]
                for document in delete_response["documentDetails"]
                if "s3" in document["identifier"]
            )

        return {
            "KnowledgeBaseId": knowledge_base_id,
            "DataSourceId": data_source_id,
            "DocumentsDiff": documents_diff,
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
            "DocumentsDiff": None,
            "IngestionJobId": ingestion_job_id,
        }


class RetryException(Exception):
    pass


def handle_check(event):
    ingestion_job = event["IngestionJob"]
    knowledge_base_id = ingestion_job["KnowledgeBaseId"]
    data_source_id = ingestion_job["DataSourceId"]

    documents_diff = ingestion_job.get("DocumentsDiff")
    if documents_diff:
        added_documents = documents_diff["Added"]
        for i in range(0, len(added_documents), 10):
            get_documents_response = bedrock_agent.get_knowledge_base_documents(
                knowledgeBaseId=knowledge_base_id,
                dataSourceId=data_source_id,
                documentIdentifiers=[
                    {
                        "dataSourceType": "S3",
                        "s3": {
                            "uri": document_identifier,
                        },
                    }
                    for document_identifier in islice(added_documents, i, i + 10)
                ],
            )
            for document in get_documents_response["documentDetails"]:
                status = document["status"]
                uri = document["identifier"].get("s3", {})["uri"]
                match status:
                    case "INDEXED":
                        pass

                    case "PENDING" | "STARTING" | "IN_PROGRESS" | "PARTIALLY_INDEXED":
                        raise RetryException()

                    case _:
                        raise Exception(f"File {uri}: Bad status '{status}'.")

        deleted_documents = documents_diff["Deleted"]
        for i in range(0, len(deleted_documents), 10):
            get_documents_response = bedrock_agent.get_knowledge_base_documents(
                knowledgeBaseId=knowledge_base_id,
                dataSourceId=data_source_id,
                documentIdentifiers=[
                    {
                        "dataSourceType": "S3",
                        "s3": {
                            "uri": document_identifier,
                        },
                    }
                    for document_identifier in islice(deleted_documents, i, i + 10)
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
