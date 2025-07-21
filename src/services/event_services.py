from models.crm_items import Event
from models.dynamo_items import EventAttendee, EventInfo, EventMetadata
from services.user_services import (update_user_attended_events,
                                    update_user_hosted_events)
from utils.logger_utils import get_logger

logger = get_logger(__name__)


async def create_event(event: Event):
    logger.info(f"Creating event: {event}")
    event_info, event_metadata, event_attendees = event.to_dynamo_item()
    EventInfo.put_item(event_info.to_payload())
    EventMetadata.put_item(event_metadata.to_payload())
    logger.info(f"Event info: {event_info}")
    logger.info(f"Event metadata: {event_metadata}")
    update_user_hosted_events(str(event_info.ownerId))
    logger.info(f"Event hosted by: {event_info.ownerId}")
    for attendee in event_attendees:
        EventAttendee.put_item(attendee.to_payload())
        update_user_attended_events(str(attendee.userId))
        logger.info(f"Event attendee: {attendee}")
