from uuid import UUID
from datetime import datetime
from typing import Optional, ClassVar

from models.base import BaseDynamoModel
from db.dynamo import dynamo_connector
from config import settings

class UserPersonalInfo(BaseDynamoModel):
    """
    User personal information model for the application.
    """
    id: str
    firstName: str
    lastName: str
    phoneNumber: str
    email: str
    avatar: Optional[str] = None
    gender: str
    table: ClassVar = dynamo_connector.Table(settings.aws_dynamodb_table_name_users)

    def to_payload(self):
        return {
            'PK': f'USER#{self.id}',
            'SK': 'USERINFO',
            'firstName': self.firstName,
            'lastName': self.lastName,
            'phoneNumber': self.phoneNumber,
            'email': self.email,
            'avatar': self.avatar,
            'gender': self.gender,
        }
    
class UserProfessionalInfo(BaseDynamoModel):
    """
    User professional information model for the application.
    """
    id: str
    jobTitle: str
    company: str
    city: str
    state: str
    table: ClassVar = dynamo_connector.Table(settings.aws_dynamodb_table_name_users)

    def to_payload(self):
        return {
            'PK': f'USER#{self.id}',
            'SK': 'USERPROF',
            'jobTitle': self.jobTitle,
            'company': self.company,
            'city': self.city,
            'state': self.state,
        }

class UserEventCount(BaseDynamoModel):
    """
    User event count model for the application.
    """
    id: str
    hostedEvents: int
    attendedEvents: int
    table: ClassVar = dynamo_connector.Table(settings.aws_dynamodb_table_name_users)

    def to_payload(self):
        return {
            'PK': f'USER#{self.id}',
            'SK': 'USEREVENTCOUNT',
            'hostedEvents': self.hostedEvents,
            'attendedEvents': self.attendedEvents,
        }
    


class EventInfo(BaseDynamoModel):
    """
    Event model for the application.
    """
    id: str
    slug: str
    title: str
    startAt: datetime
    endAt: datetime
    venue: str
    table: ClassVar = dynamo_connector.Table(settings.aws_dynamodb_table_name_events)
    ownerId: str

    def to_payload(self):
        return {
            'PK': f'EVENT#{self.id}',
            'SK': 'EVENTINFO',
            'slug': self.slug,
            'title': self.title,
            'startAt': self.startAt.strftime('%Y-%m-%d %H:%M:%S'),
            'endAt': self.endAt.strftime('%Y-%m-%d %H:%M:%S'),
            'venue': self.venue,
            'ownerId': self.ownerId,
        }

class EventMetadata(BaseDynamoModel):
    """
    Event metadata model for the application.
    """
    id : str
    description: str
    maxCapacity: int
    table: ClassVar = dynamo_connector.Table(settings.aws_dynamodb_table_name_events)

    def to_payload(self):
        return{
            'PK': f'EVENT#{self.id}',
            'SK': 'EVENTMETADATA',
            'description': self.description,
            'maxCapacity': self.maxCapacity,
        }

class EventAttendee(BaseDynamoModel):
    """
    Event attendee model for the application.
    """
    id: str
    userId: str
    table: ClassVar = dynamo_connector.Table(settings.aws_dynamodb_table_name_events)

    def to_payload(self):
        return {
            'PK': f'EVENT#{self.id}',
            'SK': 'EVENTATTENDEE',
            'userId': str(self.userId),
        }
