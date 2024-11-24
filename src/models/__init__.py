"""
Core domain models for St Mary's Fitness Management System.
This module exports all model classes for easy access.
"""

from .member import Member, MembershipType, HealthInformation
from .location import GymLocation, WorkoutZone
from .appointment import Appointment, AppointmentType
from .subscription import Subscription, PaymentFrequency
from .attendance import AttendanceRecord
from .common import Address, BaseModel

__all__ = [
    'Member', 'MembershipType', 'HealthInformation',
    'GymLocation', 'WorkoutZone',
    'Appointment', 'AppointmentType',
    'Subscription', 'PaymentFrequency',
    'AttendanceRecord',
    'Address', 'BaseModel'
]