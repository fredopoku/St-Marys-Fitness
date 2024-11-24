"""
Subscription-related models including Subscription and PaymentFrequency.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from .common import BaseModel

class PaymentFrequency(Enum):
    """Available payment frequencies"""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"

class SubscriptionStatus(Enum):
    """Status of subscriptions"""
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"

@dataclass
class Subscription(BaseModel):
    """Represents a member's subscription"""
    member_id: str
    plan_type: MembershipType
    payment_frequency: PaymentFrequency
    start_date: datetime
    end_date: datetime
    amount: float
    status: SubscriptionStatus
    payment_method: str
    auto_renew: bool = True
    last_payment_date: Optional[datetime] = None
    next_payment_date: Optional[datetime] = None

    def cancel(self):
        """Cancel the subscription"""
        self.status = SubscriptionStatus.CANCELLED
        self.auto_renew = False
        self.update()

    def renew(self, new_end_date: datetime):
        """Renew the subscription"""
        self.start_date = self.end_date
        self.end_date = new_end_date
        self.status = SubscriptionStatus.ACTIVE
        self.update()

    def is_active(self) -> bool:
        """Check if subscription is currently active"""
        now = datetime.now()
        return (self.status == SubscriptionStatus.ACTIVE and
                self.start_date <= now <= self.end_date)

    def days_until_expiry(self) -> int:
        """Calculate days until subscription expires"""
        if self.status != SubscriptionStatus.ACTIVE:
            return 0
        now = datetime.now()
        if now > self.end_date:
            return 0
        return (self.end_date - now).days