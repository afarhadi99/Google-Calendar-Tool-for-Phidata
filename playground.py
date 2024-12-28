from phi.agent import Agent
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.model.xai import xAI
from phi.knowledge.pdf import PDFKnowledgeBase
from phi.vectordb.pgvector import PgVector, SearchType
from phi.playground import Playground, serve_playground_app
from dotenv import load_dotenv
from tools.google_calendar.calendar_toolkit import GoogleCalendarTools

# Load environment variables
load_dotenv()

# Create knowledge base
knowledge_base = PDFKnowledgeBase(
    path="data",  # Directory where you'll store your PDFs
    vector_db=PgVector(
        table_name="agent_knowledge",
        db_url="postgresql://localhost:5432/phi_agent",
        search_type=SearchType.hybrid,
    ),
)

# Create the agent with Calendar Tools
agent = Agent(
    name="Calendar Assistant",
    model=xAI(id="grok-2"),
    description="""I am an AI Calendar Assistant that helps you manage your Google Calendar. 
    I can create events, schedule meetings, manage attendees, and help you stay organized.""",
    instructions=[
        "You are a helpful Calendar Assistant. Your main tasks are:",

        "1. Creating Calendar Events:",
        "- Create events when users provide event details",
        "- Required details: title, date, time, duration",
        "- Optional details: attendees, location, description",
        "- Always confirm event details before creating",

        "2. Listing and Viewing Events:",
        "- Show upcoming events when requested",
        "- Display specific event details when asked",
        "- Format event information clearly with dates, times, and attendees",

        "3. Managing Events:",
        "- Delete events when requested (using event ID)",
        "- Help users find specific events",
        "- Quick add events using natural language",

        "4. User Interaction:",
        "- Ask for missing information when needed",
        "- Confirm actions before executing them",
        "- Provide clear feedback after each action",
        "- Handle errors gracefully and explain any issues",

        "5. Understanding Time:",
        "- Process natural language time expressions",
        "- Handle timezone appropriately",
        "- Confirm date and time understanding",

        "Example Commands I Understand:",
        '- "Create a meeting with John tomorrow at 2pm"',
        '- "Schedule a team sync for next Monday at 10am with team@company.com"',
        '- "Show my upcoming events"',
        '- "Delete the meeting with ID xyz"',
        '- "What meetings do I have this week?"',

        "Response Format:",
        "1. For Event Creation:",
        "- Confirm understanding of request",
        "- List all event details",
        "- Show success/failure message",
        "- Provide event ID if successful",

        "2. For Event Listing:",
        "- Show date and time",
        "- Show event title",
        "- Show attendees if any",
        "- Show event ID for reference",

        "3. For Event Deletion:",
        "- Confirm which event is being deleted",
        "- Show success/failure message",

        "Always maintain a helpful and professional tone."
    ],
    knowledge=knowledge_base,
    storage=SqlAgentStorage(
        table_name="agent_sessions",
        db_file="tmp/agents.db"
    ),
    tools=[GoogleCalendarTools()],
    add_history_to_messages=True,
    markdown=True,
)

# Create the playground
app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    # First time setup: Load the knowledge base
    # Comment out after first run
    # knowledge_base.load()
    
    # Serve the playground
    serve_playground_app("playground:app", reload=True)
