"""
Database models for the activities management system.

Models:
- User: Represents a student or staff member
- Activity: Represents an extracurricular activity
- Enrollment: Represents a student's signup for an activity
"""

from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime


class User(SQLModel, table=True):
    """User model for students and staff."""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    enrollments: List["Enrollment"] = None


class Activity(SQLModel, table=True):
    """Activity model for extracurricular programs."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str
    schedule: str
    max_participants: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    enrollments: List["Enrollment"] = None


class Enrollment(SQLModel, table=True):
    """Enrollment model linking students to activities."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    activity_id: int = Field(foreign_key="activity.id")
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    user: Optional[User] = None
    activity: Optional[Activity] = None
