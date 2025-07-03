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
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)