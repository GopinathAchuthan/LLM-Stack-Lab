from pydantic import BaseModel, ConfigDict

class Posts(BaseModel):
    title: str
    content: str
    publish: bool = True

class PostResponse(Posts):
    id: int
    model_config = ConfigDict(from_attributes=True)