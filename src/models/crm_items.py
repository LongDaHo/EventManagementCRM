from datetime import datetime
from typing import Optional

from models.base import BaseInputModel
from models.dynamo_items import (EventAttendee, EventInfo, EventMetadata,
                                 UserPersonalInfo, UserProfessionalInfo)


class User(BaseInputModel):
    """
    User model for the application.
    """

    id: str
    firstName: str
    lastName: str
    phoneNumber: str
    email: str
    avatar: Optional[str] = None
    gender: str
    jobTitle: str
    company: str
    city: str
    state: str

    def to_dynamo_item(self):
        user_personal_info = UserPersonalInfo(
            id=self.id,
            firstName=self.firstName,
            lastName=self.lastName,
            phoneNumber=self.phoneNumber,
            email=self.email,
            avatar=self.avatar,
            gender=self.gender,
        )
        user_professional_info = UserProfessionalInfo(
            id=self.id,
            jobTitle=self.jobTitle,
            company=self.company,
            city=self.city,
            state=self.state,
        )
        return user_personal_info, user_professional_info


class Event(BaseInputModel):
    """
    Event model for the application.
    """

    id: str
    slug: str
    title: str
    description: str
    startAt: datetime
    endAt: datetime
    venue: str
    maxCapacity: int
    owner: str
    hosts: list[str]

    def to_dynamo_item(self):
        event_info = EventInfo(
            id=self.id,
            slug=self.slug,
            title=self.title,
            description=self.description,
            startAt=self.startAt,
            endAt=self.endAt,
            venue=self.venue,
            maxCapacity=self.maxCapacity,
            ownerId=self.owner,
        )
        event_metadata = EventMetadata(
            id=self.id,
            description=self.description,
            maxCapacity=self.maxCapacity,
        )
        event_attendees = [
            EventAttendee(
                id=self.id,
                userId=attendee,
            )
            for attendee in self.hosts
        ]

        return event_info, event_metadata, event_attendees
