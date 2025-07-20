from fastapi import APIRouter, Request, Header
from fastapi.responses import JSONResponse
from typing import List

from models.query_inputs import EmailRecipientQueryInput
from services.email_services import send_email, receive_sns

email_router = APIRouter(prefix="/email", tags=["email"])

@email_router.post("/send-email")
async def send_email_handler(queries: List[EmailRecipientQueryInput]):
    try:
        await send_email(queries)
        return JSONResponse(content={"message": "Email sent successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

@email_router.post("/receive-sns")
async def receive_sns_handler(request: Request, x_amz_sns_message_type: str = Header(None)):
    message = await receive_sns(request, x_amz_sns_message_type)
    return JSONResponse(content=message, status_code=200)