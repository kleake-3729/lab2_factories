from dataclasses import dataclass

@dataclass
class Email:
    """Dataclass representing an email with subject and body"""
    subject: str
    body: str
    
class Topic:
    """Dataclass representing a new topic request with topic and description"""
    topic: str
    body: str
        