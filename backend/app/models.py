"""
Database models for the FastAPI application.

This module contains SQLAlchemy models for users, job offers, skills, and their relationships.
"""
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime, Table, Boolean
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable

from app.database import Base

user_skill_association = Table(
    'user_skill_association', Base.metadata,
    Column('user_skill_id', Integer, ForeignKey('user_skills.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

class JobOffer(Base):
    """Model representing a job offer."""

    __tablename__ = 'job_offers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", back_populates="job_offers")
    email = Column(String, nullable=True, default='')
    match_score = Column(Float, default=0.0)
    reason = Column(Text, nullable=True)
    technologies_matched = Column(Text, nullable=True)
    title = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    apply_link = Column(String(1020), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        """Return string representation of JobOffer."""
        return f"<JobOffer(title={self.title}, company={self.company})>"


class Skill(Base):
    """Model representing a skill."""

    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        """Return string representation of Skill."""
        return f"<Skill(name={self.name})>"


class UserSkill(Base):
    """Model representing the relationship between users and skills."""

    __tablename__ = 'user_skills'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="user_skills")
    skills = relationship(
        'Skill', secondary=user_skill_association, back_populates='user_skills', lazy="selectin")

    def get_skill_ids(self):
        """Return list of skill IDs associated with this user skill."""
        return [skill.id for skill in self.skills]


Skill.user_skills = relationship(
    'UserSkill', secondary=user_skill_association, back_populates='skills', lazy="selectin")


class User(SQLAlchemyBaseUserTable, Base):
    """Model representing a user, extending FastAPI Users base table."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_staff = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job_offers = relationship("JobOffer", back_populates="user")
    user_skills = relationship("UserSkill", back_populates="user")

class GoogleCredentials(Base):
    __tablename__ = 'google_credentials'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)