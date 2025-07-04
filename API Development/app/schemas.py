from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class Posts(BaseModel):
    title: str
    content: str
    publish: bool = True

class PostResponse(Posts):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: int