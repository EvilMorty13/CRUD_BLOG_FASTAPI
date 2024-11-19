from pydantic import BaseModel

class PostSchema(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True

class PostDetailSchema(BaseModel):
    title: str
    content: str
    user_id: str

    class Config:
        from_attributes = True
