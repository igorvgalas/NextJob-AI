from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class JobOfferBase(BaseModel):
    """Base schema for job offers."""
    match_score: float = Field(
        default=0.0, description="Match score for the job offer")
    reason: Optional[str] = Field(
        None, description="Reason for the match score")
    technologies_matched: Optional[List[str]] = Field(
        None, description="List of matched technologies")
    title: Optional[str] = Field(None, max_length=255, description="Job title")
    company: Optional[str] = Field(
        None, max_length=255, description="Company name")
    location: Optional[str] = Field(
        None, max_length=255, description="Job location")
    description: Optional[str] = Field(None, description="Job description")
    apply_link: Optional[str] = Field(
        None, max_length=1020, description="Application link")


class JobOfferCreate(JobOfferBase):
    email: Optional[EmailStr] = Field(
        None, description="Email associated with the job offer")

class JobOfferBulkCreate(BaseModel):
    job_offers: List[JobOfferCreate]

class JobOfferRead(JobOfferBase):
    id: int
    user_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


class SkillBase(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the skill")


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    id: int

    class Config:
        orm_mode = True


class UserSkillBase(BaseModel):
    user_id: int

class UserSkill(UserSkillBase):
    id: int
    user_id: int
    skills: List[Skill]

    class Config:
        orm_mode = True

class UserSkillCreate(UserSkillBase):
    user_id: int 
    skill_ids: List[int] 

class UserSkillUpdate(BaseModel):
    skill_ids: List[int]


class UserSkillStat(BaseModel):
    username: str
    num_skills: int


class UserRead(BaseUser[int]):
    id: int
    email: EmailStr
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_staff: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class UserCreate(BaseUserCreate):
    first_name: Optional[str]
    last_name: Optional[str]
    is_staff: Optional[bool] = False

class UserUpdate(BaseUserUpdate):
    username: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class GoogleCredentials(BaseModel):
    user_id: int
    access_token: str
    refresh_token: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class GoogleCredentialsCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_token: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class GoogleCredentialsUpdate(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }