import json
from typing import List

import httpx
from fastapi import Header, Request

from models.query_inputs import EmailRecipientQueryInput, UserQueryInput
from services.user_services import get_user_based_on_query
from utils.email_utils import send_email_via_ses
from utils.logger_utils import get_logger

logger = get_logger(__name__)


async def send_email(queries: List[EmailRecipientQueryInput]):
    user_query_inputs = []
    for query in queries:
        user_query_input = UserQueryInput(
            company=query.company,
            jobTitle=query.jobTitle,
            city=query.city,
            state=query.state,
            minEventAttendedCount=query.minEventAttendedCount,
            maxEventAttendedCount=query.maxEventAttendedCount,
        )
        user_query_inputs.append(user_query_input)
    responses = await get_user_based_on_query(user_query_inputs)
    for response in responses:
        for user in response["users"]:
            await send_email_via_ses(user["email"], query.subject, query.body)


async def receive_sns(request: Request, x_amz_sns_message_type: str = Header(None)):
    body = await request.json()
    message_type = x_amz_sns_message_type

    if message_type == "SubscriptionConfirmation":
        # Confirm the subscription
        token_url = body["SubscribeURL"]
        async with httpx.AsyncClient() as client:
            await client.get(token_url)
        return {"message": "Subscription confirmed"}

    elif message_type == "Notification":
        sns_message = json.loads(body["Message"])
        logger.info("📩 Received SES event:", sns_message)

        # Handle different types
        event_type = sns_message.get("notificationType")
        if event_type == "Delivery":
            logger.info("✅ Email delivered to:", sns_message["delivery"]["recipients"])
        elif event_type == "Bounce":
            logger.info("❌ Email bounced:", sns_message["bounce"]["bouncedRecipients"])
        elif event_type == "Complaint":
            logger.info(
                "⚠️ Complaint received:",
                sns_message["complaint"]["complainedRecipients"],
            )

        return {"message": "Notification processed"}

    return {"message": "Unhandled SNS message type"}
