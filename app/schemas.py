from pydantic import BaseModel, EmailStr
from datetime import datetime

class BlogBase(BaseModel):
    title: str
    content: str
    published: bool=True

class BlogCreate(BlogBase):
    pass


class BlogResponse(BlogBase):
    id: int
    created_at: datetime
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