# tools/google_calendar/calendar_toolkit.py

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from phi.tools import Toolkit
from .calendar_auth import GoogleCalendarAuth
from dateutil import parser
import pytz

class GoogleCalendarTools(Toolkit):
    def __init__(self):
        super().__init__(name="google_calendar_tools")
        self.service = GoogleCalendarAuth.get_calendar_service()
        
        # Register all the methods
        self.register(self.create_event)
        self.register(self.list_events)
        self.register(self.get_event)
        self.register(self.delete_event)
        self.register(self.quick_add_event)

    def create_event(self, 
                    title: str,
                    start_time: str,
                    duration_minutes: int = 60,
                    guests: Optional[List[str]] = None,
                    description: Optional[str] = None,
                    location: Optional[str] = None,
                    timezone: str = "UTC") -> str:
        """Creates a calendar event.
        
        Args:
            title: Title of the event
            start_time: Start time (can be natural language like "tomorrow at 2pm")
            duration_minutes: Duration in minutes
            guests: List of attendee email addresses
            description: Description of the event
            location: Location of the event
            timezone: Timezone for the event
        """
        try:
            # Parse the start datetime
            start_dt = parser.parse(start_time)
            # Calculate end time based on duration
            end_dt = start_dt + timedelta(minutes=duration_minutes)
            
            event_body = {
                'summary': title,
                'location': location,
                'description': description,
                'start': {
                    'dateTime': start_dt.isoformat(),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_dt.isoformat(),
                    'timeZone': timezone,
                }
            }

            if guests:
                event_body['attendees'] = [{'email': email.strip()} for email in guests]

            created_event = self.service.events().insert(
                calendarId='primary',
                sendUpdates='all',
                body=event_body
            ).execute()

            response = (
                f"✅ Event Created Successfully!\n\n"
                f"**Title**: {title}\n"
                f"**Start**: {start_dt.strftime('%Y-%m-%d %I:%M %p')}\n"
                f"**End**: {end_dt.strftime('%Y-%m-%d %I:%M %p')}\n"
            )
            
            if guests:
                response += f"**Attendees**: {', '.join(guests)}\n"
            if location:
                response += f"**Location**: {location}\n"
            if description:
                response += f"**Description**: {description}\n"
                
            response += f"\n**Event ID**: `{created_event.get('id')}`"
            return response
        except Exception as e:
            return f"❌ Failed to create event: {str(e)}"

    def list_events(self, 
                   days: int = 7,
                   max_results: int = 10) -> str:
        """Lists upcoming calendar events.
        
        Args:
            days: Number of days to look ahead
            max_results: Maximum number of events to return
        """
        try:
            now = datetime.utcnow()
            time_max = (now + timedelta(days=days)).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now.isoformat() + 'Z',
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            if not events:
                return "📅 No upcoming events found."
            
            response = f"📅 **Upcoming Events** (Next {days} days)\n\n"
            for event in events:
                start = parser.parse(event['start'].get('dateTime', event['start'].get('date')))
                response += f"### {event['summary']}\n"
                response += f"**When**: {start.strftime('%Y-%m-%d %I:%M %p')}\n"
                
                if event.get('location'):
                    response += f"**Where**: {event['location']}\n"
                if event.get('attendees'):
                    attendees = [a['email'] for a in event['attendees']]
                    response += f"**Attendees**: {', '.join(attendees)}\n"
                response += f"**Event ID**: `{event['id']}`\n\n"
            
            return response
        except Exception as e:
            return f"❌ Failed to list events: {str(e)}"

    def get_event(self, event_id: str) -> str:
        """Gets details of a specific event.
        
        Args:
            event_id: ID of the event to retrieve
        """
        try:
            event = self.service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()

            start = parser.parse(event['start'].get('dateTime', event['start'].get('date')))
            end = parser.parse(event['end'].get('dateTime', event['end'].get('date')))
            
            response = f"📅 **Event Details**\n\n"
            response += f"### {event['summary']}\n"
            response += f"**Start**: {start.strftime('%Y-%m-%d %I:%M %p')}\n"
            response += f"**End**: {end.strftime('%Y-%m-%d %I:%M %p')}\n"
            
            if event.get('location'):
                response += f"**Location**: {event['location']}\n"
            if event.get('description'):
                response += f"**Description**: {event['description']}\n"
            if event.get('attendees'):
                response += "\n**Attendees**:\n"
                for attendee in event['attendees']:
                    status = attendee.get('responseStatus', 'no response')
                    response += f"- {attendee['email']} ({status})\n"
            
            response += f"\n**Event ID**: `{event['id']}`"
            return response
        except Exception as e:
            return f"❌ Failed to get event: {str(e)}"

    def delete_event(self, event_id: str) -> str:
        """Deletes a calendar event.
        
        Args:
            event_id: ID of the event to delete
        """
        try:
            # First get the event to confirm it exists
            event = self.service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            # Then delete it
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id,
                sendUpdates='all'
            ).execute()
            
            return f"✅ Event '{event.get('summary')}' has been deleted successfully"
        except Exception as e:
            return f"❌ Failed to delete event: {str(e)}"

    def quick_add_event(self, text: str) -> str:
        """Quickly adds an event using natural language.
        
        Args:
            text: Natural language description (e.g., "Meeting with John tomorrow at 3pm")
        """
        try:
            event = self.service.events().quickAdd(
                calendarId='primary',
                text=text,
                sendUpdates='all'
            ).execute()
            
            start = parser.parse(event['start'].get('dateTime', event['start'].get('date')))
            
            response = f"✅ **Event Created Successfully!**\n\n"
            response += f"**Title**: {event.get('summary')}\n"
            response += f"**When**: {start.strftime('%Y-%m-%d %I:%M %p')}\n"
            if event.get('location'):
                response += f"**Where**: {event['location']}\n"
            response += f"\n**Event ID**: `{event.get('id')}`"
            return response
        except Exception as e:
            return f"❌ Failed to create event: {str(e)}"
