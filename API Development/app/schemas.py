from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr
from datetime import datetime

class Posts(BaseModel):
    title: str
    content: str
    publish: bool = True

class PostResponse(Posts):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str