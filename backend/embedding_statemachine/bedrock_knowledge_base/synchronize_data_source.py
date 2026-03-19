import os

from app.utils import (
    get_bedrock_agent_client,
)

DOCUMENT_BUCKET = os.environ.get("DOCUMENT_BUCKET")
bedrock_agent = get_bedrock_agent_client()


def handler(event, context):
    """Perform data source synchronization for a Knowledge Base."""
    match event["Action"]:
        case "Ingest":
            return handle_ingest(event)

        case "Check":
            return handle_check(event)

        case _ as e:
            raise Exception(f"Unknown action {e}")


def handle_ingest(event):
    """Start a full data source synchronization job for a Knowledge Base.

    Always uses start_ingestion_job (the standard full sync) rather than
    ingest_knowledge_base_documents (direct ingestion). The full sync is
    compatible with all vector store backends including S3 Vectors, correctly
    handles additions, modifications, and deletions, and matches the reliable
    code path used by linked S3 bucket sources.
    """
    knowledge_base_id = event["KnowledgeBaseId"]
    data_source_id = event["DataSourceId"]

    start_job_response = bedrock_agent.start_ingestion_job(
        knowledgeBaseId=knowledge_base_id,
        dataSourceId=data_source_id,
    )
    ingestion_job_id = start_job_response["ingestionJob"]["ingestionJobId"]

    return {
        "KnowledgeBaseId": knowledge_base_id,
        "DataSourceId": data_source_id,
        "IngestionJobId": ingestion_job_id,
    }


class RetryException(Exception):
    pass


def handle_check(event):
    """Check for the completion of the synchronization job."""
    ingestion_job = event["IngestionJob"]
    knowledge_base_id = ingestion_job["KnowledgeBaseId"]
    data_source_id = ingestion_job["DataSourceId"]
    ingestion_job_id = ingestion_job.get("IngestionJobId")

    if not ingestion_job_id:
        raise Exception("Invalid parameters: IngestionJobId is required.")

    get_job_response = bedrock_agent.get_ingestion_job(
        knowledgeBaseId=knowledge_base_id,
        dataSourceId=data_source_id,
        ingestionJobId=ingestion_job_id,
    )
    status = get_job_response["ingestionJob"]["status"]
    match status:
        case "COMPLETE":
            return

        case "STARTING" | "IN_PROGRESS":
            raise RetryException()

        case _:
            raise Exception(
                f"Ingestion Job '{ingestion_job_id}': Bad status '{status}'."
            )
