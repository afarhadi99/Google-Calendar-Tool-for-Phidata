# tools/gmail/gmail_toolkit.py

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
from datetime import datetime
from phi.tools import Toolkit
from .gmail_auth import GmailAuth
from .gmail_types import EmailMessage, EmailDraft, EmailLabel, EmailResponse, EmailAddress

class GmailTools(Toolkit):
    def __init__(self):
        super().__init__(name="gmail_tools")
        self.service = GmailAuth.get_gmail_service()
        
        # Register all the methods
        self.register(self.send_email)
        self.register(self.create_draft)
        self.register(self.list_emails)
        self.register(self.read_email)
        self.register(self.create_label)
        self.register(self.list_labels)
        self.register(self.apply_label)
        self.register(self.search_emails)
        self.register(self.get_email_thread)

    def send_email(self, 
                  to: str,
                  subject: str,
                  body: str,
                  cc: Optional[str] = None,
                  bcc: Optional[str] = None,
                  html: bool = False) -> str:
        """Sends an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            cc: CC recipient email addresses (comma-separated)
            bcc: BCC recipient email addresses (comma-separated)
            html: Whether to send as HTML
        
        Returns:
            str: Success/failure message
        """
        try:
            message = MIMEMultipart() if html else MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc
                
            if html:
                message.attach(MIMEText(body, 'html'))
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            sent_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return f"✅ Email sent successfully. Message ID: {sent_message['id']}"
        except Exception as e:
            return f"❌ Failed to send email: {str(e)}"

    def create_draft(self, 
                    to: str,
                    subject: str,
                    body: str,
                    cc: Optional[str] = None,
                    bcc: Optional[str] = None,
                    html: bool = False) -> str:
        """Creates an email draft.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            cc: CC recipient email addresses (comma-separated)
            bcc: BCC recipient email addresses (comma-separated)
            html: Whether to create as HTML
        
        Returns:
            str: Success/failure message with draft ID
        """
        try:
            message = MIMEMultipart() if html else MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc
                
            if html:
                message.attach(MIMEText(body, 'html'))
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            draft = self.service.users().drafts().create(
                userId='me',
                body={
                    'message': {
                        'raw': raw_message
                    }
                }
            ).execute()
            
            return f"✅ Draft created successfully. Draft ID: {draft['id']}"
        except Exception as e:
            return f"❌ Failed to create draft: {str(e)}"

    def list_emails(self, 
               max_results: int = 10,
               label_ids: Optional[List[str]] = None) -> str:
        """Lists emails in the inbox.
        
        Args:
            max_results: Maximum number of emails to return
            label_ids: List of label IDs to filter by
        
        Returns:
            str: Formatted list of emails
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                labelIds=label_ids or ['INBOX']
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                return "📭 No emails found."
            
            response = "📧 **Recent Emails**:\n\n"
            for idx, msg in enumerate(messages, 1):
                try:
                    message = self.service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='metadata',
                        metadataHeaders=['From', 'Subject', 'Date']
                    ).execute()
                    
                    headers = message['payload']['headers']
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                    date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                    
                    # Clean and format the output
                    subject = subject.replace('\r', ' ').replace('\n', ' ').strip()
                    sender = sender.replace('\r', ' ').replace('\n', ' ').strip()
                    
                    # Format the date
                    try:
                        parsed_date = datetime.strptime(date.split('(')[0].strip(), '%a, %d %b %Y %H:%M:%S %z')
                        date = parsed_date.strftime('%Y-%m-%d %H:%M')
                    except:
                        # If date parsing fails, clean up the raw date string
                        date = date.replace('\r', ' ').replace('\n', ' ').strip()
                    
                    response += f"### {idx}. {subject}\n"
                    response += f"**From**: {sender}\n"
                    response += f"**Date**: {date}\n"
                    response += f"**ID**: `{message['id']}`\n\n"
                
                except Exception as e:
                    response += f"### {idx}. Error loading email\n"
                    response += f"**Error**: {str(e)}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Failed to list emails: {str(e)}"

    def read_email(self, message_id: str) -> str:
        """Reads a specific email.
        
        Args:
            message_id: ID of the email to read
        
        Returns:
            str: Formatted email content
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Get message body
            if 'parts' in message['payload']:
                parts = message['payload']['parts']
                body = next((
                    base64.urlsafe_b64decode(part['body']['data']).decode()
                    for part in parts
                    if part['mimeType'] in ['text/plain', 'text/html']
                    and 'data' in part['body']
                ), "No readable content")
            else:
                body = base64.urlsafe_b64decode(
                    message['payload']['body'].get('data', '')).decode()
            
            response = f"## {subject}\n\n"
            response += f"**From**: {sender}\n"
            response += f"**Date**: {date}\n"
            response += f"**Labels**: {', '.join(message.get('labelIds', []))}\n\n"
            response += "### Content:\n\n"
            response += body
            
            return response
        except Exception as e:
            return f"❌ Failed to read email: {str(e)}"

    def create_label(self, label: EmailLabel) -> str:
        """Creates a new label.
        
        Args:
            label: EmailLabel object containing label details
        
        Returns:
            str: Success/failure message
        """
        try:
            label_body = {
                'name': label.name,
                'labelListVisibility': label.label_list_visibility,
                'messageListVisibility': label.message_list_visibility
            }
            
            if label.color:
                label_body['color'] = label.color
            
            created_label = self.service.users().labels().create(
                userId='me',
                body=label_body
            ).execute()
            
            return f"✅ Label created successfully. Label ID: {created_label['id']}"
        except Exception as e:
            return f"❌ Failed to create label: {str(e)}"

    def list_labels(self) -> str:
        """Lists all labels.
        
        Returns:
            str: Formatted list of labels
        """
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            if not labels:
                return "No labels found."
            
            response = "📑 Labels:\n\n"
            for label in labels:
                response += f"- {label['name']} (ID: `{label['id']}`)\n"
            
            return response
        except Exception as e:
            return f"❌ Failed to list labels: {str(e)}"

    def apply_label(self, 
                   message_id: str,
                   label_ids: List[str],
                   remove_labels: Optional[List[str]] = None) -> str:
        """Applies or removes labels from an email.
        
        Args:
            message_id: ID of the email
            label_ids: List of label IDs to apply
            remove_labels: List of label IDs to remove
        
        Returns:
            str: Success/failure message
        """
        try:
            body = {
                'addLabelIds': label_ids,
                'removeLabelIds': remove_labels or []
            }
            
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body=body
            ).execute()
            
            return f"✅ Labels updated successfully for message: {message_id}"
        except Exception as e:
            return f"❌ Failed to update labels: {str(e)}"

    def search_emails(self, 
                     query: str,
                     max_results: int = 10) -> str:
        """Searches for emails using Gmail query syntax.
        
        Args:
            query: Gmail search query
            max_results: Maximum number of results to return
        
        Returns:
            str: Formatted search results
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                return "🔍 No matching emails found."
            
            response = f"🔍 Search Results for: '{query}'\n\n"
            for msg in messages:
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()
                
                headers = message['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                
                response += f"### {subject}\n"
                response += f"**From**: {sender}\n"
                response += f"**Date**: {date}\n"
                response += f"**ID**: `{message['id']}`\n\n"
            
            return response
        except Exception as e:
            return f"❌ Failed to search emails: {str(e)}"

    def get_email_thread(self, thread_id: str) -> str:
        """Gets all messages in an email thread.
        
        Args:
            thread_id: ID of the thread to retrieve
        
        Returns:
            str: Formatted thread content
        """
        try:
            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id
            ).execute()
            
            if not thread['messages']:
                return "No messages found in thread."
            
            response = "📧 Email Thread:\n\n"
            for message in thread['messages']:
                headers = message['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                
                response += f"### {subject}\n"
                response += f"**From**: {sender}\n"
                response += f"**Date**: {date}\n"
                
                # Get message body
                if 'parts' in message['payload']:
                    parts = message['payload']['parts']
                    body = next((
                        base64.urlsafe_b64decode(part['body']['data']).decode()
                        for part in parts
                        if part['mimeType'] in ['text/plain', 'text/html']
                        and 'data' in part['body']
                    ), "No readable content")
                else:
                    body = base64.urlsafe_b64decode(
                        message['payload']['body'].get('data', '')).decode()
                
                response += "\n---\n"
                response += body
                response += "\n---\n\n"
            
            return response
        except Exception as e:
            return f"❌ Failed to get thread: {str(e)}"
