from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    nick_name: Optional[str] = None

class UserResponse(UserBase):
    user_id: int
    google_id: str
    created_at: datetime

    class Config:
        from_attributes = True