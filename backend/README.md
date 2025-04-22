# Backend API

Written in Python with [FastAPI](https://fastapi.tiangolo.com/).

## Getting started

- To get started, we need to deploy resources to create DynamoDB / Bedrock resource. To deploy, please see [Deploy using CDK](../README.md#deploy-using-cdk).
- Create [poetry](https://python-poetry.org/) environment on your local machine

```sh
cd backend
python3 -m venv .venv  # Optional (If you don't want to install poetry on your env)
source .venv/bin/activate  # Optional (If you don't want to install poetry on your env)
pip install poetry
poetry install
```

- Configure environment variables

```sh
export CONVERSATION_TABLE_NAME=BedrockChatStack-DatabaseConversationTablexxxx
export BOT_TABLE_NAME=BedrockChatStack-DatabaseBotTablexxxx
export ACCOUNT=yyyy
export REGION=ap-northeast-1
export BEDROCK_REGION=us-east-1
export DOCUMENT_BUCKET=bedrockchatstack-documentbucketxxxxxxx
export LARGE_MESSAGE_BUCKET=bedrockchatstack-largemessagebucketxxx
export USER_POOL_ID=xxxxxxxxx
export CLIENT_ID=xxxxxxxxx
export OPENSEARCH_DOMAIN_ENDPOINT=https://abcdefghijklmnopqrst.aa-region-1.aoss.amazonaws.com
```

- Configure CDK configration.
Local development requires OpenSearch data access permissions for the IAM role to be used. You can set this parameter in either `cdk/cdk.json` or `cdk/parameter.ts`.

  This configuration grants the following permissions:

  For the OpenSearch Collection:

    ```
    "aoss:DescribeCollectionItems",
    "aoss:CreateCollectionItems", 
    "aoss:DeleteCollectionItems",
    "aoss:UpdateCollectionItems"
    ```

  For the index:

    ```
    "aoss:DescribeIndex", 
    "aoss:ReadDocument", 
    "aoss:WriteDocument",
    "aoss:CreateIndex",
    "aoss:DeleteIndex",
    "aoss:UpdateIndex"
    ```

  Example in cdk/cdk.json:
    ```
    json 

    {
      "devAccessIamRoleArn": "arn:aws:iam::123456789012:role/<role name>"
    }
    ```

## Launch local server

```sh
poetry run uvicorn app.main:app  --reload --host 0.0.0.0 --port 8000
```

- To refer the specification, access to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for [Swagger](https://swagger.io/) and [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for [Redoc](https://github.com/Redocly/redoc).

## Unit test

```sh
poetry run python tests/test_bedrock.py
poetry run python tests/test_repositories/test_conversation.py
```
