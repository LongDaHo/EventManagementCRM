from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models.crm_items import Event
from services.event_services import create_event

event_router = APIRouter(prefix="/events", tags=["events"])


@event_router.post("/create-event")
async def create_event_handler(event: Event):
    await create_event(event)
    return JSONResponse(
        content={"message": "Event created successfully"}, status_code=200
    )
