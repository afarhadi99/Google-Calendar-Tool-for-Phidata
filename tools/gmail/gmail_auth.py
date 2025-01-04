# tools/gmail/gmail_auth.py

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Optional

class GmailAuth:
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.labels',
        'https://www.googleapis.com/auth/gmail.metadata'
    ]
    
    @staticmethod
    def get_gmail_service():
        """Gets an authorized Gmail API service instance."""
        creds = None
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists('gmail_token.pickle'):
            with open('gmail_token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    # If refresh fails, force new authentication
                    creds = None
            
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', GmailAuth.SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('gmail_token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)
