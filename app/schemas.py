from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
class BlogBase(BaseModel):
    title: str
    content: str
    published: bool=False

class BlogCreate(BlogBase):
    pass


class BlogResponse(BlogBase):
    id: int
    created_at: datetime
    owner_id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]