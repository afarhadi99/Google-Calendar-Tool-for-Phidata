<div align="center">
  <img src="https://cdn.prod.website-files.com/66e0d4ef58ba78f56e23564e/66e0d4ef58ba78f56e2356a9_Logo.avif" alt="Phidata Logo" width="200"/>
  <img src="https://fonts.gstatic.com/s/i/productlogos/calendar_2020q4/v13/web-64dp/logo_calendar_2020q4_color_2x_web_64dp.png" alt="Google Calendar Logo" width="200"/>

  # Google Calendar Tool for Phidata
</div>

## Overview

This project integrates Google Calendar functionality with Phidata's Agent framework, creating a powerful calendar management assistant. The tool is built as a custom toolkit that allows Phidata agents to interact with Google Calendar API, enabling features such as creating events, managing schedules, and handling calendar operations.

The project is structured with a main `playground.py` file that serves as the entry point and demonstration interface, while the core calendar functionality is implemented as a toolkit in the `tools/google_calendar` directory. The playground provides an interactive chat interface where users can communicate with the calendar assistant using natural language.

### Project Structure

````bash
CalendarAgent/
├── .env
├── requirements.txt
├── playground.py
├── tools/
│   ├── __init__.py
│   └── google_calendar/
│       ├── __init__.py
│       ├── calendar_toolkit.py
│       ├── calendar_auth.py
│       └── calendar_types.py
````

## Requirements

- [Python 3.11](https://www.python.org/downloads/) or higher
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) for running PgVector
- [Google Cloud Console Account](https://console.cloud.google.com/)
- [Phidata Account](https://phidata.app/)
- IDE such as [Visual Studio Code](https://code.visualstudio.com/)

## Setting Up

1. Clone the repository:
````bash
git clone <repository-url>
cd CalendarAgent
````

2. Create a `.env` file and add your API keys:
````env
XAI_API_KEY=your-xai-api-key
PHI_API_KEY=your-phi-api-key
````

3. Install requirements:
````bash
pip install -r requirements.txt
````

4. Start PgVector:
````bash
docker run -d -e POSTGRES_DB=phi_agent -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e PGDATA=/var/lib/postgresql/data/pgdata -v pgvolume:/var/lib/postgresql/data -p 5432:5432 --name pgvector phidata/pgvector:16
````

5. Set up Google Calendar API credentials (see below)

6. Run the playground:
````bash
python playground.py
````

## Getting OAuth 2.0 Credentials from Google Cloud Platform

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Create a new project or select an existing one

3. Enable the Google Calendar API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

4. Configure the OAuth consent screen:
   - Go to "APIs & Services" > "OAuth consent screen"
   - Select "Internal" if you're in an organization, or "External" for personal use
   - Fill in the required information (App name, User support email, Developer contact)
   - Add "/auth/calendar" and "/auth/calendar.events" to the scopes
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

The first time you run the application, it will open a browser window for authentication. After authenticating, the application will save the token for future use.
