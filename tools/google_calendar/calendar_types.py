# tools/google_calendar/calendar_types.py

from typing import List, Optional
from pydantic import BaseModel

class EventGuest(BaseModel):
    """Represents a guest/attendee for an event"""
    email: str
    optional: bool = False

class EventDateTime(BaseModel):
    """Represents date and time for an event"""
    date_time: str
    time_zone: str = "UTC"

class CalendarEvent(BaseModel):
    """Represents a calendar event"""
    name: str
    start: EventDateTime
    end: EventDateTime
    guests: Optional[List[EventGuest]] = None
    description: Optional[str] = None
    location: Optional[str] = None

class EventResponse(BaseModel):
    """Standard response format for event operations"""
    success: bool
    message: str
    event_id: Optional[str] = None
