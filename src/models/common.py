"""
Common models and base classes used across the system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class BaseModel:
    """Base model class with common attributes and methods"""
    id: str
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize ID if not provided"""
        if not self.id:
            self.id = str(uuid.uuid4())

    def update(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()

@dataclass
class Address:
    """Represents a physical address"""
    street: str
    city: str
    state: str
    postal_code: str
    country: str

    def __str__(self) -> str:
        """Return formatted address string"""
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}, {self.country}"