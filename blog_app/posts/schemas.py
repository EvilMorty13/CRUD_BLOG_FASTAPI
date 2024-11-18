from pydantic import BaseModel

class PostSchema(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True
