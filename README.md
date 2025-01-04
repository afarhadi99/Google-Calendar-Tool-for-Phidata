<div align="center">
  <img src="https://cdn.prod.website-files.com/66e0d4ef58ba78f56e23564e/66e0d4ef58ba78f56e2356a9_Logo.avif" alt="Phidata Logo" width="200"/>
  <img src="https://fonts.gstatic.com/s/i/productlogos/calendar_2020q4/v13/web-64dp/logo_calendar_2020q4_color_2x_web_64dp.png" alt="Google Calendar Logo" width="200"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Gmail_icon_%282020%29.svg/2560px-Gmail_icon_%282020%29.svg.png" alt="Google Gmail Logo" width="200"/>

  # Google Calendar and Gmail Tool for Phidata
</div>

## Overview

This project integrates both Google Calendar and Gmail functionality with Phidata's Agent framework, creating a powerful email and calendar management assistant. The tool is built as a custom toolkit that allows Phidata agents to interact with both Google Calendar and Gmail APIs, enabling features such as creating events, managing schedules, sending emails, and handling various email and calendar operations.

The project is structured with a main `playground.py` file that serves as the entry point and demonstration interface, while the core functionality is implemented as toolkits in the `tools/google_calendar` and `tools/gmail` directories. The playground provides an interactive chat interface where users can communicate with the assistant using natural language.

### Project Structure

```bash
CalendarAgent/
├── .env
├── requirements.txt
├── playground.py
├── tools/
│   ├── __init__.py
│   ├── google_calendar/
│   │   ├── __init__.py
│   │   ├── calendar_toolkit.py
│   │   ├── calendar_auth.py
│   │   └── calendar_types.py
│   └── gmail/
│       ├── __init__.py
│       ├── gmail_toolkit.py
│       ├── gmail_auth.py
│       └── gmail_types.py
```

## Features

### Calendar Features
- Create and manage calendar events
- Schedule meetings with multiple attendees
- View upcoming events
- Delete and modify existing events
- Quick add events using natural language
- Handle recurring events
- Manage event details (location, description, etc.)

### Gmail Features
- Send and receive emails
- Create email drafts
- Search through emails
- Manage email labels
- View email threads
- Handle HTML and plain text emails
- Manage CC and BCC recipients
- Create and apply email labels

## Requirements

- [Python 3.11](https://www.python.org/downloads/) or higher
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) for running PgVector
- [Google Cloud Console Account](https://console.cloud.google.com/)
- [Phidata Account](https://phidata.app/)
- IDE such as [Visual Studio Code](https://code.visualstudio.com/)

## Setting Up

1. Clone the repository:
```bash
git clone <repository-url>
cd CalendarAgent
```

2. Create a `.env` file and add your API keys:
```env
OPENAI_API_KEY=your-openai-api-key
PHI_API_KEY=your-phi-api-key
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Start PgVector:
```bash
docker run -d -e POSTGRES_DB=phi_agent -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e PGDATA=/var/lib/postgresql/data/pgdata -v pgvolume:/var/lib/postgresql/data -p 5432:5432 --name pgvector phidata/pgvector:16
```

5. Set up Google OAuth 2.0 credentials (see below)

6. Run the playground:
```bash
python playground.py
```

## Getting OAuth 2.0 Credentials from Google Cloud Platform

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Create a new project or select an existing one

3. Enable the required APIs:
   - Navigate to "APIs & Services" > "Library"
   - Search for and enable:
     - "Google Calendar API"
     - "Gmail API"

4. Configure the OAuth consent screen:
   - Go to "APIs & Services" > "OAuth consent screen"
   - Select "Internal" if you're in an organization, or "External" for personal use
   - Fill in the required information (App name, User support email, Developer contact)
   - Add the following scopes:
     - "/auth/calendar"
     - "/auth/calendar.events"
     - "/auth/gmail.modify"
     - "/auth/gmail.compose"
     - "/auth/gmail.send"
     - "/auth/gmail.labels"
     - "/auth/gmail.metadata"
   - Add your email as a test user

5. Create OAuth 2.0 Client ID:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Give it a name
   - Click "Create"

6. Download the credentials:
   - After creation, download the client configuration file
   - Rename it to `credentials.json`
   - Place it in your project's root directory

The first time you run the application, it will open a browser window for authentication. After authenticating, the application will save separate tokens for Gmail and Calendar access for future use.

## Usage Examples

### Calendar Operations
```python
# Create an event
"Create a meeting with John tomorrow at 2pm"

# List upcoming events
"Show my calendar for next week"

# Update an event
"Update the location of tomorrow's meeting to Conference Room A"
```

### Gmail Operations
```python
# Send an email
"Send an email to john@example.com about the project update"

# Search emails
"Find all emails from Sarah about the budget"

# Create a label
"Create a new label called 'Project X'"
```

## Security Considerations

- The application uses OAuth 2.0 for secure authentication
- Tokens are stored locally and encrypted
- Sensitive operations require explicit confirmation
- All API calls are made over HTTPS
- User consent is required for accessing Gmail and Calendar data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.