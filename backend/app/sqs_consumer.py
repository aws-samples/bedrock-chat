import json

from app.routes.schemas.conversation import (
    ChatInput,
)
from app.usecases.chat import chat, chat_output_from_message


def handler(event, context):
    """SQS consumer.
    This is used for async invocation for published api.
    """
    for record in event["Records"]:
        message_body = json.loads(record["body"])
        chat_input = ChatInput(**message_body)
        user_id = f"PUBLISHED_API#{chat_input.bot_id}"

        conversation, message = chat(user_id=user_id, chat_input=chat_input)
        chat_result = chat_output_from_message(
            conversation=conversation,
            message=message,
        )
        print(chat_result)

    return {"statusCode": 200, "body": json.dumps("Processing completed")}
