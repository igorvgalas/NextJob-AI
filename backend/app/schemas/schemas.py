from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class JobOfferBase(BaseModel):
    id: int
    user_id: int | None = None
    email: str | None = None
    match_score: float
    reason: str | None = None
    technologies_matched: str | None = None
    title: str | None = None
    company: str | None = None
    location: str | None = None
    description: str | None = None
    apply_link: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobOfferPage(BaseModel):
    count: int
    next: str | None
    previous: str | None
    results: list[JobOfferBase]


class JobOfferCreate(JobOfferBase):
    email: Optional[EmailStr] = Field(
        default=None, description="Email associated with the job offer")


class JobOfferBulkCreate(BaseModel):
    job_offers: List[JobOfferCreate]


class JobOfferRead(JobOfferBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SkillBase(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the skill")


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserSkillBase(BaseModel):
    user_id: int


class UserSkill(UserSkillBase):
    id: int
    user_id: int
    skills: List[Skill]

    model_config = ConfigDict(from_attributes=True)


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
    scope: Optional[str] = None
    token_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GoogleCredentialsCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    token_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class GoogleCredentialsUpdate(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    token_type: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
