# tools/gmail/gmail_types.py

from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class EmailAddress(BaseModel):
    name: Optional[str] = None
    email: str

class EmailMessage(BaseModel):
    to: List[EmailAddress]
    subject: str
    body: str
    cc: Optional[List[EmailAddress]] = None
    bcc: Optional[List[EmailAddress]] = None
    html: bool = False

class EmailDraft(BaseModel):
    message: EmailMessage
    draft_id: Optional[str] = None

class EmailLabel(BaseModel):
    name: str
    label_list_visibility: Optional[str] = "labelShow"
    message_list_visibility: Optional[str] = "show"
    color: Optional[Dict[str, str]] = None

class EmailThread(BaseModel):
    thread_id: str
    history_id: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = None

class EmailResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
